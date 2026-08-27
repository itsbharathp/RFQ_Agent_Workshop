"""
Challenge 4: The Tactician
Agentic AI — Planning and Optimisation Pattern

Build a Claude-powered agent that receives a Work Order and produces
an optimised RFQ vendor selection plan.

Usage:
    export ANTHROPIC_API_KEY="your-key-here"
    python starter.py --wo WO-2024-0187 --month 10

    # Run the challenge twist (compare three months)
    python starter.py --compare
"""

import json
import argparse
import pandas as pd
import anthropic
from pathlib import Path

DATA = Path("../../output_v2")

HEALTHY_SCORE_THRESHOLD = 70   # minimum health score to be considered for invite
TARGET_VENDORS_PER_RFQ  = 8   # standard pool size

# ─── Load data ────────────────────────────────────────────────────────────────

def load_all_data() -> dict[str, pd.DataFrame]:
    return {
        "work_orders":  pd.read_csv(DATA / "07_work_orders.csv"),
        "wo_items":     pd.read_csv(DATA / "08_work_order_items.csv"),
        "vendors":      pd.read_csv(DATA / "01_vendors.csv"),
        "health":       pd.read_csv(DATA / "23_vendor_health_scores.csv"),
        "signals":      pd.read_csv(DATA / "04_market_signals.csv", parse_dates=["date"]),
        "commodities":  pd.read_csv(DATA / "03_commodity_prices.csv", parse_dates=["week_start"]),
        "rfq_events":   pd.read_csv(DATA / "09_rfq_events.csv"),
    }


# ─── Tool implementations ────────────────────────────────────────────────────

def tool_get_work_order(work_order_id: str, db: dict) -> dict:
    """Return work order details and line items."""
    wo = db["work_orders"]
    items = db["wo_items"]

    wo_row = wo[wo["work_order_id"] == work_order_id]
    if wo_row.empty:
        # Fall back to a random one from the correct era if not found
        wo_row = wo.sample(1)

    wo_data = wo_row.iloc[0].to_dict()
    wo_items = items[items["work_order_id"] == work_order_id].to_dict("records")

    return {
        "work_order": wo_data,
        "items": wo_items,
        "primary_category": items[items["work_order_id"] == work_order_id]["category"].mode().iloc[0]
                            if len(wo_items) > 0 else "Mechanical Parts",
    }


def tool_get_vendor_pool(category: str, db: dict) -> dict:
    """Return all vendors in a category with their base profile."""
    vendors = db["vendors"]
    pool = vendors[vendors["category"] == category][[
        "vendor_id", "vendor_name", "behavioral_archetype", "risk_tier",
        "is_new_vendor", "relationship_arc", "relationship_years",
        "base_price_index", "base_response_rate", "base_otd_rate",
        "financial_health_score", "forecast_eligible"
    ]].copy()
    return {
        "category": category,
        "total_vendors": len(pool),
        "vendors": pool.to_dict("records")
    }


def tool_get_vendor_health(vendor_id: str, month_index: int, db: dict) -> dict:
    """Return current health score and trend for a vendor."""
    h = db["health"]
    row = h[(h["vendor_id"] == vendor_id) & (h["month_index"] == month_index)]
    if row.empty:
        # Try nearest available month
        vendor_rows = h[h["vendor_id"] == vendor_id]
        if vendor_rows.empty:
            return {"vendor_id": vendor_id, "error": "No health data found"}
        row = vendor_rows.iloc[[-1]]

    data = row.iloc[0].to_dict()
    return {
        "vendor_id": vendor_id,
        "composite_score": data.get("composite_health_score"),
        "trend": data.get("trend_3mo"),
        "alert_flag": data.get("alert_flag"),
        "alert_reason": data.get("alert_reason"),
        "payment_reliability": data.get("payment_reliability_score"),
        "win_rate_score": data.get("win_rate_score"),
        "admin_burden_score": data.get("admin_burden_score"),
        "relationship_arc": data.get("relationship_arc"),
        "thin_data_flag": data.get("thin_data_flag"),
    }


def tool_get_market_signals(category: str, db: dict) -> dict:
    """Return recent market signals relevant to a procurement category."""
    signals = db["signals"]

    # Map category to commodity keywords for filtering
    cat_keywords = {
        "Electrical Components": ["Electrical", "PCB", "Servo", "copper", "Neodymium"],
        "Mechanical Parts": ["Steel", "Aluminium", "Bearing", "Titanium"],
        "Raw Materials": ["Steel", "Aluminium", "Copper", "Stainless", "HDPE"],
    }
    keywords = cat_keywords.get(category, [])

    # Filter signals that mention relevant commodities
    relevant = signals[
        signals["affected_commodities"].str.contains("|".join(keywords), case=False, na=False) |
        signals["full_text"].str.contains("|".join(keywords), case=False, na=False)
    ].tail(5)

    return {
        "category": category,
        "n_signals": len(relevant),
        "signals": relevant[["date", "signal_type", "source", "full_text",
                             "sentiment_score", "cascade_potential"]].to_dict("records")
    }


def tool_get_commodity_prices(category: str, weeks_back: int, db: dict) -> dict:
    """Return recent commodity price data for a category."""
    commodities = db["commodities"]

    cat_filter = {
        "Electrical Components": ["Electrical Components"],
        "Mechanical Parts": ["Mechanical Parts"],
        "Raw Materials": ["Raw Materials"],
    }
    cats = cat_filter.get(category, [category])

    recent = commodities[
        commodities["categories"].str.contains("|".join(cats), na=False)
    ].tail(weeks_back * len(cats))

    # Summarise by commodity
    summary = recent.groupby("commodity").agg(
        latest_price=("price", "last"),
        price_4w_ago=("price", lambda x: x.iloc[-min(4, len(x))] if len(x) >= 4 else x.iloc[0]),
        shock_flag_recent=("shock_flag", "max"),
    ).reset_index()

    summary["pct_change_4w"] = (
        (summary["latest_price"] - summary["price_4w_ago"]) / summary["price_4w_ago"] * 100
    ).round(1)

    return {
        "category": category,
        "weeks_back": weeks_back,
        "commodities": summary.to_dict("records"),
        "any_shock_active": bool(summary["shock_flag_recent"].any()),
    }


def tool_get_competitor_activity(month_index: int, db: dict) -> dict:
    """
    Return a signal about competitor (Hexagon AG) procurement activity.
    Higher activity means tighter vendor capacity.
    """
    # The Dec 2024 signal (month ~11) flags Hexagon capacity ramp
    # We model competitor pressure as higher in months 11-17
    competitor_active_months = list(range(11, 18))
    is_active = month_index in competitor_active_months

    return {
        "month_index": month_index,
        "hexagon_ag_activity": "high" if is_active else "normal",
        "vendor_capacity_pressure": "elevated" if is_active else "normal",
        "note": (
            "Hexagon AG announced 30% capacity ramp (Dec 2024); competing for shared vendor pool."
            if is_active else
            "No unusual competitor activity detected this period."
        )
    }


def tool_create_rfq_plan(plan: dict, db: dict) -> dict:
    """
    Finalise the RFQ plan. This is the 'write' tool — calling it commits the plan.
    In a real system this would write to the database. Here it validates and returns.
    """
    required_keys = ["work_order_id", "vendor_shortlist", "rfq_terms"]
    for key in required_keys:
        if key not in plan:
            return {"success": False, "error": f"Missing required field: {key}"}

    plan["status"] = "planned"
    plan["n_vendors_shortlisted"] = len(plan.get("vendor_shortlist", []))
    return {"success": True, "plan": plan, "message": "RFQ plan finalised successfully"}


# ─── Tool registry ────────────────────────────────────────────────────────────

TOOL_DEFINITIONS = [
    {
        "name": "get_work_order",
        "description": "Get details of a specific work order including items, category, urgency, and budget. Always call this first.",
        "input_schema": {
            "type": "object",
            "properties": {
                "work_order_id": {"type": "string", "description": "Work order ID e.g. 'WO-2024-0187'"}
            },
            "required": ["work_order_id"]
        }
    },
    {
        "name": "get_vendor_pool",
        "description": "Get all vendors in a procurement category with their base performance profile.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": ["Mechanical Parts", "Electrical Components", "Raw Materials"]}
            },
            "required": ["category"]
        }
    },
    {
        "name": "get_vendor_health",
        "description": "Get the current health score, trend, and alert status for a specific vendor.",
        "input_schema": {
            "type": "object",
            "properties": {
                "vendor_id": {"type": "string", "description": "Vendor ID e.g. 'V002'"},
                "month_index": {"type": "integer", "description": "Current month (0=Jan 2024, 17=Jun 2025)"}
            },
            "required": ["vendor_id", "month_index"]
        }
    },
    {
        "name": "get_market_signals",
        "description": "Get recent market intelligence signals (policy changes, price movements, geopolitical events) relevant to a procurement category.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": ["Mechanical Parts", "Electrical Components", "Raw Materials"]}
            },
            "required": ["category"]
        }
    },
    {
        "name": "get_commodity_prices",
        "description": "Get recent commodity price trends for a category. Useful for detecting price shocks that will affect bid values.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": ["Mechanical Parts", "Electrical Components", "Raw Materials"]},
                "weeks_back": {"type": "integer", "description": "How many weeks of data to retrieve (default: 8)"}
            },
            "required": ["category"]
        }
    },
    {
        "name": "get_competitor_activity",
        "description": "Check whether Hexagon AG (Meridian's main competitor) is actively procuring in the same category, increasing vendor capacity pressure.",
        "input_schema": {
            "type": "object",
            "properties": {
                "month_index": {"type": "integer", "description": "Current month index"}
            },
            "required": ["month_index"]
        }
    },
    {
        "name": "create_rfq_plan",
        "description": "Finalise and commit the RFQ vendor selection plan. Call this LAST after all analysis is complete.",
        "input_schema": {
            "type": "object",
            "properties": {
                "plan": {
                    "type": "object",
                    "description": "The complete RFQ plan with vendor_shortlist, rfq_terms, market_context, risk_flags, and adaptation_notes",
                    "properties": {
                        "work_order_id": {"type": "string"},
                        "category": {"type": "string"},
                        "urgency": {"type": "string"},
                        "budget_ceiling_usd": {"type": "number"},
                        "vendor_shortlist": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "vendor_id": {"type": "string"},
                                    "vendor_name": {"type": "string"},
                                    "health_score": {"type": "number"},
                                    "invite_priority": {"type": "integer"},
                                    "rationale": {"type": "string"}
                                }
                            }
                        },
                        "n_vendors_to_invite": {"type": "integer"},
                        "rfq_terms": {"type": "object"},
                        "market_context": {"type": "string"},
                        "risk_flags": {"type": "array", "items": {"type": "string"}},
                        "adaptation_notes": {"type": "string"}
                    },
                    "required": ["work_order_id", "vendor_shortlist", "rfq_terms"]
                }
            },
            "required": ["plan"]
        }
    },
]


# ─── Tool dispatcher ──────────────────────────────────────────────────────────

def dispatch_tool(tool_name: str, tool_input: dict, month_index: int, db: dict) -> str:
    if tool_name == "get_work_order":
        result = tool_get_work_order(tool_input["work_order_id"], db)
    elif tool_name == "get_vendor_pool":
        result = tool_get_vendor_pool(tool_input["category"], db)
    elif tool_name == "get_vendor_health":
        result = tool_get_vendor_health(tool_input["vendor_id"], tool_input.get("month_index", month_index), db)
    elif tool_name == "get_market_signals":
        result = tool_get_market_signals(tool_input["category"], db)
    elif tool_name == "get_commodity_prices":
        result = tool_get_commodity_prices(tool_input["category"], tool_input.get("weeks_back", 8), db)
    elif tool_name == "get_competitor_activity":
        result = tool_get_competitor_activity(tool_input.get("month_index", month_index), db)
    elif tool_name == "create_rfq_plan":
        result = tool_create_rfq_plan(tool_input["plan"], db)
    else:
        result = {"error": f"Unknown tool: {tool_name}"}

    return json.dumps(result, default=str)


# ─── System prompt ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
TODO: Write the system prompt for the Tactician agent.

The Tactician is a strategic procurement planning agent for Meridian Industrial Systems.
It receives a Work Order and must produce an optimal RFQ vendor selection plan.

Your system prompt should define:

1. The agent's mission and decision authority
   - It MUST produce a plan (not just a report)
   - It MUST adapt the plan when the standard playbook won't work

2. The investigation sequence (what to check and in what order)
   - What to look at first (work order details)
   - What to assess next (vendor pool health)
   - What contextual factors to consider (market, competitor)

3. Decision rules for vendor selection
   - How to rank vendors when some are unhealthy
   - What to do when fewer than 8 healthy vendors are available
   - How to weight health trends vs point-in-time scores
   - Special handling for new_proving vs collapse arc vendors

4. When to adapt standard RFQ terms
   - When to extend bid windows (low pool health, market uncertainty)
   - When to adjust evaluation weights (price shock active = reduce price weight)
   - When to add special conditions

5. The planning mindset
   - The agent should be decisive: it should make recommendations, not hedge
   - It should explain its adaptations clearly in adaptation_notes
   - risk_flags should be specific (name the vendor or market event), not generic

6. Output requirements
   - Must call create_rfq_plan as the final action
   - The plan must have a vendor_shortlist with at least 3 vendors (minimum viable RFQ)
   - Each vendor in the shortlist needs an invite_priority and a rationale
"""


# ─── Main agent loop ──────────────────────────────────────────────────────────

def run_tactician(work_order_id: str, month_index: int, db: dict) -> dict | None:
    """
    TODO: Implement the Tactician agentic loop.

    This is the same tool-use loop pattern as Challenge 3, with one key difference:
    the agent MUST call create_rfq_plan before it can stop.

    The loop ends when:
    - The agent calls create_rfq_plan AND gets a success response, OR
    - The agent returns stop_reason="end_turn" (extract plan from response if tool was called)

    Return the finalised plan dict, or None if the agent failed.

    Tip: track whether create_rfq_plan was called in the loop.
    If the agent tries to stop without calling it, inject a message asking it to finalise.
    """
    client = anthropic.Anthropic()

    messages = [
        {
            "role": "user",
            "content": (
                f"Plan the vendor selection for Work Order {work_order_id}. "
                f"Current month is {month_index} (0=Jan 2024). "
                f"Analyse the vendor pool, check market conditions, and produce a complete RFQ plan. "
                f"You must call create_rfq_plan to finalise your recommendation."
            )
        }
    ]

    print(f"\n[Tactician] Planning RFQ for {work_order_id} at month {month_index}...")

    final_plan = None

    # TODO: Implement the agentic loop here (same pattern as Challenge 3)
    # Extra requirement: detect when create_rfq_plan is called and capture the result

    return final_plan


# ─── Challenge twist: compare three months ───────────────────────────────────

def run_comparison(db: dict) -> None:
    """
    Run the Tactician for three different market conditions and compare the plans.
    """
    # Find a work order from each era
    wo = db["work_orders"]

    scenarios = [
        (wo[wo["month_index"] == 5].iloc[0]["work_order_id"],  5,  "Pre-constraint (Jun 2024)"),
        (wo[wo["month_index"] == 10].iloc[0]["work_order_id"], 10, "Constraint active (Nov 2024)"),
        (wo[wo["month_index"] == 15].iloc[0]["work_order_id"], 15, "Late period (Apr 2025)"),
    ]

    plans = []
    for wo_id, mo, label in scenarios:
        print(f"\n{'='*60}")
        print(f"SCENARIO: {label}")
        print(f"{'='*60}")
        plan = run_tactician(wo_id, mo, db)
        if plan:
            plans.append({"scenario": label, "month": mo, "plan": plan})

    print(f"\n{'='*60}")
    print("COMPARISON SUMMARY")
    print(f"{'='*60}")
    for p in plans:
        plan = p["plan"]
        n_vendors = len(plan.get("vendor_shortlist", []))
        adaptation = plan.get("adaptation_notes", "None")
        risks = plan.get("risk_flags", [])
        print(f"\n{p['scenario']}:")
        print(f"  Vendors invited: {n_vendors}")
        print(f"  Risk flags: {len(risks)}")
        print(f"  Adaptations: {adaptation[:150]}...")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Meridian RFQ Tactician Agent")
    parser.add_argument("--wo", type=str, help="Work Order ID to plan")
    parser.add_argument("--month", type=int, default=10,
                        help="Month index (0=Jan 2024, 17=Jun 2025)")
    parser.add_argument("--compare", action="store_true",
                        help="Run the three-scenario comparison (Challenge Twist)")
    args = parser.parse_args()

    print("Loading data...")
    db = load_all_data()

    if args.compare:
        run_comparison(db)
        return

    # Pick a default work order if none specified
    if not args.wo:
        wo = db["work_orders"]
        # Find one near the requested month
        candidate = wo[wo["month_index"] == args.month]
        if candidate.empty:
            candidate = wo.iloc[[0]]
        args.wo = candidate.iloc[0]["work_order_id"]
        print(f"No WO specified — using {args.wo} (month {args.month})")

    plan = run_tactician(args.wo, args.month, db)

    if plan:
        print(f"\n{'='*60}")
        print("TACTICIAN — FINAL RFQ PLAN")
        print(f"{'='*60}")
        print(json.dumps(plan, indent=2, default=str))

        output_path = f"rfq_plan_{args.wo}_m{args.month}.json"
        with open(output_path, "w") as f:
            json.dump(plan, f, indent=2, default=str)
        print(f"\nPlan saved to {output_path}")
    else:
        print("\n[ERROR] Tactician did not produce a plan.")


if __name__ == "__main__":
    main()
