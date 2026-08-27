"""
Challenge 3: The Watchdog
Agentic AI — Monitoring and Detection Pattern

Build a Claude-powered agent that reads vendor health data and generates
structured alerts for at-risk vendors.

Usage:
    export ANTHROPIC_API_KEY="your-key-here"
    python starter.py

    # Run for a specific month (0=Jan 2024, 8=Sep 2024, 17=Jun 2025)
    python starter.py --month 10
"""

import json
import argparse
import pandas as pd
import anthropic
from pathlib import Path

DATA = Path("../../output_v2")

# Alert severity thresholds
SCORE_CRITICAL  = 60
SCORE_HIGH      = 70
SCORE_MEDIUM    = 75
TREND_DECLINING = "declining"

# ─── Load all data at startup (tools query from these DataFrames) ──────────────

def load_all_data() -> dict[str, pd.DataFrame]:
    return {
        "health":   pd.read_csv(DATA / "23_vendor_health_scores.csv", parse_dates=["month"]),
        "payments": pd.read_csv(DATA / "20_payment_events.csv"),
        "disputes": pd.read_csv(DATA / "16_vendor_disputes.csv"),
        "invites":  pd.read_csv(DATA / "10_rfq_vendor_invites.csv"),
        "eval":     pd.read_csv(DATA / "13_bid_evaluation.csv"),
        "vendors":  pd.read_csv(DATA / "01_vendors.csv"),
    }


# ─── Tool implementations (read-only, query the DataFrames) ──────────────────

def tool_get_health_snapshot(month_index: int, db: dict) -> dict:
    """Return all vendors' health scores for a given month."""
    h = db["health"]
    snapshot = h[h["month_index"] == month_index][[
        "vendor_id", "vendor_name", "composite_health_score",
        "trend_3mo", "alert_flag", "alert_reason",
        "payment_reliability_score", "win_rate_score",
        "admin_burden_score", "relationship_arc", "thin_data_flag"
    ]].copy()
    return {"month_index": month_index, "vendors": snapshot.to_dict("records")}


def tool_get_vendor_trend(vendor_id: str, n_months: int, current_month: int, db: dict) -> dict:
    """Return the last n_months of health scores for a vendor."""
    h = db["health"]
    start = max(0, current_month - n_months + 1)
    trend = h[
        (h["vendor_id"] == vendor_id) &
        (h["month_index"] >= start) &
        (h["month_index"] <= current_month)
    ][["month_index", "composite_health_score", "trend_3mo",
       "payment_reliability_score", "win_rate_score", "admin_burden_score"]].copy()
    return {
        "vendor_id": vendor_id,
        "n_months": n_months,
        "history": trend.to_dict("records"),
        "score_change": (
            float(trend["composite_health_score"].iloc[-1]) -
            float(trend["composite_health_score"].iloc[0])
        ) if len(trend) >= 2 else None
    }


def tool_get_payment_history(vendor_id: str, n_months: int, current_month: int, db: dict) -> dict:
    """Return recent payment events for a vendor (how Meridian paid them)."""
    p = db["payments"]
    start = max(0, current_month - n_months + 1)
    payments = p[
        (p["vendor_id"] == vendor_id) &
        (p["month_index"] >= start) &
        (p["month_index"] <= current_month)
    ][["month_index", "po_value_usd", "payment_status",
       "days_late", "days_early", "meridian_stress_index"]].copy()

    summary = {
        "vendor_id": vendor_id,
        "total_payments": len(payments),
        "on_time_pct": float((payments["payment_status"] == "on_time").mean()) if len(payments) else None,
        "avg_days_late": float(payments["days_late"].mean()) if len(payments) else None,
        "late_payments": len(payments[payments["payment_status"].isin(["late", "disputed"])]),
        "recent_payments": payments.tail(6).to_dict("records"),
    }
    return summary


def tool_get_dispute_history(vendor_id: str, db: dict) -> dict:
    """Return all disputes for a vendor."""
    d = db["disputes"]
    disputes = d[d["vendor_id"] == vendor_id][[
        "dispute_id", "dispute_date", "reason", "claimed_usd", "resolved", "resolution"
    ]].copy()
    return {
        "vendor_id": vendor_id,
        "total_disputes": len(disputes),
        "open_disputes": len(disputes[disputes["resolved"] == False]),
        "disputes": disputes.to_dict("records"),
    }


def tool_get_rfq_participation(vendor_id: str, n_months: int, current_month: int, db: dict) -> dict:
    """Return recent RFQ invite and win history for a vendor."""
    inv  = db["invites"]
    evl  = db["eval"]
    start = max(0, current_month - n_months + 1)

    inv_recent = inv[
        (inv["vendor_id"] == vendor_id) &
        (inv["month_index"] >= start)
    ]
    evl_recent = evl[
        (evl["vendor_id"] == vendor_id) &
        (evl["month_index"] >= start)
    ]

    n_invited   = len(inv_recent)
    n_responded = int(inv_recent["responded"].sum()) if "responded" in inv_recent.columns and n_invited else 0
    n_won       = int(evl_recent["selected"].sum()) if len(evl_recent) else 0

    return {
        "vendor_id": vendor_id,
        "months_covered": n_months,
        "n_invited": n_invited,
        "n_responded": n_responded,
        "n_bids_won": n_won,
        "response_rate": round(n_responded / n_invited, 2) if n_invited else None,
        "win_rate": round(n_won / n_invited, 2) if n_invited else None,
    }


# ─── Tool registry (defines what Claude can call) ────────────────────────────

TOOL_DEFINITIONS = [
    {
        "name": "get_health_snapshot",
        "description": "Get all vendors' health scores for a specific month. Use this first to identify which vendors need investigation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "month_index": {"type": "integer", "description": "Month index (0=Jan 2024, 8=Sep 2024, 17=Jun 2025)"}
            },
            "required": ["month_index"]
        }
    },
    {
        "name": "get_vendor_trend",
        "description": "Get the health score history for a specific vendor over recent months. Use this to understand if deterioration is new or established.",
        "input_schema": {
            "type": "object",
            "properties": {
                "vendor_id": {"type": "string", "description": "Vendor ID e.g. 'V001'"},
                "n_months": {"type": "integer", "description": "How many months of history to retrieve (default: 6)"}
            },
            "required": ["vendor_id"]
        }
    },
    {
        "name": "get_payment_history",
        "description": "Get Meridian's payment history to a specific vendor. Late payments from Meridian cause vendor disengagement.",
        "input_schema": {
            "type": "object",
            "properties": {
                "vendor_id": {"type": "string", "description": "Vendor ID"},
                "n_months": {"type": "integer", "description": "How many months of history (default: 6)"}
            },
            "required": ["vendor_id"]
        }
    },
    {
        "name": "get_dispute_history",
        "description": "Get all disputes for a vendor (late delivery, quality rejection). Disputes correlate with relationship deterioration.",
        "input_schema": {
            "type": "object",
            "properties": {
                "vendor_id": {"type": "string", "description": "Vendor ID"}
            },
            "required": ["vendor_id"]
        }
    },
    {
        "name": "get_rfq_participation",
        "description": "Get how often a vendor is invited to RFQs, responds, and wins. Declining participation is an early warning sign.",
        "input_schema": {
            "type": "object",
            "properties": {
                "vendor_id": {"type": "string", "description": "Vendor ID"},
                "n_months": {"type": "integer", "description": "How many months of history (default: 6)"}
            },
            "required": ["vendor_id"]
        }
    },
]


# ─── Tool dispatcher ──────────────────────────────────────────────────────────

def dispatch_tool(tool_name: str, tool_input: dict, current_month: int, db: dict) -> str:
    """Route tool calls to the correct function and return JSON string."""
    n_months = tool_input.get("n_months", 6)

    if tool_name == "get_health_snapshot":
        result = tool_get_health_snapshot(tool_input["month_index"], db)
    elif tool_name == "get_vendor_trend":
        result = tool_get_vendor_trend(tool_input["vendor_id"], n_months, current_month, db)
    elif tool_name == "get_payment_history":
        result = tool_get_payment_history(tool_input["vendor_id"], n_months, current_month, db)
    elif tool_name == "get_dispute_history":
        result = tool_get_dispute_history(tool_input["vendor_id"], db)
    elif tool_name == "get_rfq_participation":
        result = tool_get_rfq_participation(tool_input["vendor_id"], n_months, current_month, db)
    else:
        result = {"error": f"Unknown tool: {tool_name}"}

    return json.dumps(result, default=str)


# ─── System prompt ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
TODO: Write the system prompt for the Watchdog agent.

The agent monitors vendor health for Meridian Industrial Systems (a CNC machine manufacturer).
It has access to tools to query health scores, payment history, disputes, and RFQ participation.

Your system prompt should:
1. Define the agent's role and objective
2. Explain what makes a vendor "at risk" (not just score thresholds — also trends)
3. Describe the investigation process (which tools to call first, which to call conditionally)
4. Define the alert output format (severity levels, what to include in root_cause)
5. Tell the agent when NOT to alert (thin data, stable low-scorers, new vendors)
6. Set the tone: specific and actionable, not vague or generic

HINT: The agent should be opinionated. "Monitor closely" is not a recommendation.
"""


# ─── Alert extraction ─────────────────────────────────────────────────────────

def extract_alerts_from_response(response_text: str) -> list[dict]:
    """
    TODO: Parse the agent's final text response into structured Alert objects.

    The agent's response will contain alert information in some format.
    You need to extract it into a list of dicts with these keys:
      vendor_id, vendor_name, alert_severity, composite_score,
      trend, root_cause, supporting_evidence, recommended_action, urgency

    Options:
    A) Ask the agent to output JSON (easiest — update the system prompt to request this)
    B) Parse structured text with regex or string splitting
    C) Make a second Claude call to extract structured data from the agent's prose

    Choice is yours. Option A is recommended for this exercise.
    """
    # Your code here
    return []


# ─── Main agent loop ──────────────────────────────────────────────────────────

def run_watchdog(month_index: int, db: dict) -> list[dict]:
    """
    TODO: Implement the agentic loop.

    The loop pattern:
    1. Build the initial user message: "Analyse vendor health for month {month_index}"
    2. Call Claude with tools enabled
    3. If the response contains tool_use blocks, dispatch each tool and collect results
    4. Append tool results to messages and call Claude again
    5. Repeat until Claude returns a final text response (no more tool calls)
    6. Extract and return alerts from the final response

    This is the standard tool-use agentic loop. The loop continues as long as
    Claude keeps calling tools. It stops when Claude returns stop_reason="end_turn"
    without any tool_use blocks.

    Reference: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
    """
    client = anthropic.Anthropic()

    messages = [
        {
            "role": "user",
            "content": f"Run vendor health analysis for month_index={month_index}. "
                       f"Identify all at-risk vendors and generate alerts with root cause analysis."
        }
    ]

    print(f"\n[Watchdog] Analysing month {month_index}...")

    # TODO: Implement the agentic loop here
    # Skeleton:
    #
    # while True:
    #     response = client.messages.create(
    #         model="claude-sonnet-4-6",
    #         max_tokens=4096,
    #         system=SYSTEM_PROMPT,
    #         tools=TOOL_DEFINITIONS,
    #         messages=messages,
    #     )
    #
    #     # Add assistant response to messages
    #     messages.append({"role": "assistant", "content": response.content})
    #
    #     if response.stop_reason == "end_turn":
    #         # Extract final text response
    #         # Extract and return alerts
    #         break
    #
    #     if response.stop_reason == "tool_use":
    #         # Collect all tool results
    #         tool_results = []
    #         for block in response.content:
    #             if block.type == "tool_use":
    #                 print(f"  -> Calling tool: {block.name}({block.input})")
    #                 result = dispatch_tool(block.name, block.input, month_index, db)
    #                 tool_results.append({
    #                     "type": "tool_result",
    #                     "tool_use_id": block.id,
    #                     "content": result,
    #                 })
    #
    #         # Add tool results to messages
    #         messages.append({"role": "user", "content": tool_results})

    return []   # replace with your extracted alerts


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Meridian Vendor Watchdog Agent")
    parser.add_argument("--month", type=int, default=10,
                        help="Month index to analyse (0=Jan 2024, 17=Jun 2025)")
    args = parser.parse_args()

    print("Loading data...")
    db = load_all_data()
    print(f"Data loaded. Running watchdog for month_index={args.month}...\n")

    alerts = run_watchdog(args.month, db)

    print(f"\n{'='*60}")
    print(f"WATCHDOG REPORT — Month {args.month}")
    print(f"{'='*60}")
    print(f"Alerts generated: {len(alerts)}")
    print()

    for i, alert in enumerate(alerts, 1):
        print(f"Alert {i}: [{alert.get('alert_severity','?')}] {alert.get('vendor_name','?')}")
        print(f"  Score:     {alert.get('composite_score','?')}")
        print(f"  Trend:     {alert.get('trend','?')}")
        print(f"  Root cause: {alert.get('root_cause','?')}")
        print(f"  Action:    {alert.get('recommended_action','?')}")
        print(f"  Urgency:   {alert.get('urgency','?')}")
        print()

    # Save alerts to JSON
    if alerts:
        output_path = f"watchdog_alerts_month{args.month}.json"
        with open(output_path, "w") as f:
            json.dump(alerts, f, indent=2, default=str)
        print(f"Alerts saved to {output_path}")


if __name__ == "__main__":
    main()
