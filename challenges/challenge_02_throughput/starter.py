"""
Challenge 2: What's It Worth?
Throughput Accounting — Meridian Industrial Systems

Build a monthly TA model and quantify the $ impact of the vendor health constraint.

Usage:
    python starter.py

Outputs:
    ta_model.csv         — full monthly model
    ta_summary.csv       — pre vs post comparison
    ta_charts.png        — visualisations
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA = Path("../../output_v2")

# Assumption constants (see BRIEFING.md)
OE_PER_CLARIFICATION_ROUND = 150.00   # USD
INVENTORY_HOLDING_RATE_PM  = 0.008    # 0.8% per month
CONSTRAINT_START_MONTH     = 8        # September 2024 (month_index 8)

# ─── Data loading ─────────────────────────────────────────────────────────────

def load_data() -> dict[str, pd.DataFrame]:
    so   = pd.read_csv(DATA / "05_sales_orders.csv")
    po   = pd.read_csv(DATA / "14_purchase_orders.csv")
    pay  = pd.read_csv(DATA / "20_payment_events.csv")
    bur  = pd.read_csv(DATA / "22_rfq_admin_burden.csv")
    bids = pd.read_csv(DATA / "12_bids.csv")
    return dict(so=so, po=po, pay=pay, bur=bur, bids=bids)


def print_summary(data: dict) -> None:
    for name, df in data.items():
        print(f"{name:6s}: {len(df):>6,} rows  |  {list(df.columns)}")


# ─── T: Throughput ────────────────────────────────────────────────────────────
#
# Throughput = Revenue - Truly Variable Cost
# Revenue    = sum of sales order values per month
# TVC        = sum of purchase order values per month (direct material spend)
#
# Note: match month_index, not calendar date — both tables have month_index column.

def compute_throughput(so: pd.DataFrame, po: pd.DataFrame) -> pd.DataFrame:
    """
    TODO:
    1. Group so by month_index, sum total_value_usd → revenue per month
    2. Group po by month_index, sum po_value_usd    → tvc per month
    3. Join on month_index (use .merge with how='outer').fillna(0)
    4. Compute throughput = revenue - tvc
    5. Return a DataFrame with columns: month_index, revenue, tvc, throughput

    Hint: some months may have SOs but no POs (or vice versa) — outer join is safer.
    """
    # Your code here
    pass


# ─── I: Investment (cash tied up) ─────────────────────────────────────────────
#
# Proxy: for each payment event, the cash was "tied up" for (payment_terms_days + days_late) days.
# We approximate monthly investment as: sum(po_value_usd * days_late / 30) for that month.
# This captures the extra working capital consumed by late payments.

def compute_investment(pay: pd.DataFrame) -> pd.DataFrame:
    """
    TODO:
    1. Compute tied_up_months = days_late / 30   (fractional months of cash tied up)
    2. Compute investment_contribution = po_value_usd * tied_up_months * INVENTORY_HOLDING_RATE_PM
       (this is the cost of the tied-up cash, not the gross amount)
    3. Group by month_index, sum investment_contribution → investment_cost per month
    4. Return DataFrame with columns: month_index, investment_cost

    Optional: also return total_po_value and avg_days_late per month for context.
    """
    # Your code here
    pass


# ─── OE: Operating Expense friction ──────────────────────────────────────────
#
# The team's salaries are fixed (not a variable cost here).
# But extra clarification rounds represent ADDITIONAL capacity consumed.
# We model this as: clarification_rounds × OE_PER_CLARIFICATION_ROUND per RFQ.

def compute_oe_friction(bur: pd.DataFrame) -> pd.DataFrame:
    """
    TODO:
    1. Filter bur to responded == True (only engaged vendors)
    2. Compute oe_friction = clarification_rounds * OE_PER_CLARIFICATION_ROUND
    3. Group by month_index, sum oe_friction
    4. Return DataFrame with columns: month_index, oe_friction

    Note: this is the INCREMENTAL OE from the constraint, not total OE.
    """
    # Your code here
    pass


# ─── Combine into monthly TA model ───────────────────────────────────────────

def build_ta_model(throughput_df, investment_df, oe_df) -> pd.DataFrame:
    """
    TODO:
    1. Merge the three DataFrames on month_index (outer join, fill nulls with 0)
    2. Compute:
       - net_profit_proxy  = throughput - oe_friction
       - roi_proxy         = net_profit_proxy / investment_cost  (handle division by zero)
    3. Add a column constraint_period = month_index >= CONSTRAINT_START_MONTH
    4. Return the full monthly model
    """
    # Your code here
    pass


# ─── Before vs After comparison ──────────────────────────────────────────────

def compare_periods(ta_model: pd.DataFrame) -> pd.DataFrame:
    """
    TODO:
    1. Split ta_model into pre-constraint (month_index < 8) and post-constraint (>= 8)
    2. For each period, compute:
       - mean monthly throughput
       - mean monthly OE friction
       - total throughput
       - total investment cost
    3. Return a comparison DataFrame with one row per period
    4. Print the T gap: "T dropped by $X/month on average after Sep 2024"
    """
    # Your code here
    pass


# ─── Bid price spread analysis (stretch goal) ────────────────────────────────

def analyse_bid_spread(bids: pd.DataFrame) -> pd.DataFrame:
    """
    STRETCH GOAL:
    1. Group bids by rfq_id: compute max_bid, min_bid, bid_count, spread = max - min
    2. Join with month_index (it's already on bids)
    3. Group by month_index: mean spread, mean bid_count
    4. Plot: does spread narrow when bid_count drops?
    5. Return the monthly summary
    """
    # Your code here
    pass


# ─── The breakeven statement ──────────────────────────────────────────────────

def breakeven_statement(ta_model: pd.DataFrame) -> str:
    """
    TODO:
    1. Compute total_t_lost = (pre_period_mean_T - post_period_mean_T) × n_post_months
    2. Return a formatted string:
       "Total T lost in constraint period: $X
        Meridian could invest up to $Y fixing vendor health and still break even,
        where $Y = total_t_lost."

    This is the business case for the CFO.
    """
    # Your code here
    return "TODO: fill in the breakeven statement"


# ─── Charts ───────────────────────────────────────────────────────────────────

def plot_ta_model(ta_model: pd.DataFrame) -> None:
    """
    TODO:
    Create a 2×2 chart showing:
    [0,0] Monthly Throughput — with vertical line at month 8, shaded post-constraint region
    [0,1] Monthly OE Friction — bar chart, same axis scale
    [1,0] T vs TVC stacked area (to show the margin being squeezed)
    [1,1] Net Profit Proxy over time

    Save to ta_charts.png
    """
    # Your code here
    pass


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Loading data...")
    data = load_data()
    print_summary(data)
    print()

    print("Computing Throughput (T)...")
    t_df = compute_throughput(data["so"], data["po"])

    print("Computing Investment cost (I)...")
    i_df = compute_investment(data["pay"])

    print("Computing OE friction...")
    oe_df = compute_oe_friction(data["bur"])

    print("Building monthly TA model...")
    ta = build_ta_model(t_df, i_df, oe_df)

    if ta is not None:
        ta.to_csv("ta_model.csv", index=False)
        print(f"Saved ta_model.csv ({len(ta)} rows)")
        print()

        print("=== PERIOD COMPARISON ===")
        summary = compare_periods(ta)
        if summary is not None:
            summary.to_csv("ta_summary.csv", index=False)
            print(summary.to_string())
        print()

        print("=== BREAKEVEN STATEMENT ===")
        print(breakeven_statement(ta))
        print()

        print("Generating charts...")
        plot_ta_model(ta)
        print("Saved ta_charts.png")

    print()
    print("=== STRETCH: Bid Spread Analysis ===")
    spread = analyse_bid_spread(data["bids"])
    if spread is not None:
        print(spread.head(18).to_string())
