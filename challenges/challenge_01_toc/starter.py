"""
Challenge 1: Find the Bottleneck
Theory of Constraints — Meridian Industrial Systems

Run this file as-is first. It loads the data and prints shapes.
Then work through each TODO section in order.

Usage:
    python starter.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

DATA = Path("../../output_v2")

# ─── Data loading (done for you) ──────────────────────────────────────────────

def load_data() -> dict[str, pd.DataFrame]:
    rfq      = pd.read_csv(DATA / "09_rfq_events.csv", parse_dates=["issue_date", "bid_deadline"])
    invites  = pd.read_csv(DATA / "10_rfq_vendor_invites.csv")
    burden   = pd.read_csv(DATA / "22_rfq_admin_burden.csv")
    health   = pd.read_csv(DATA / "23_vendor_health_scores.csv", parse_dates=["month"])
    vendors  = pd.read_csv(DATA / "01_vendors.csv")
    bids     = pd.read_csv(DATA / "12_bids.csv")
    return dict(rfq=rfq, invites=invites, burden=burden, health=health,
                vendors=vendors, bids=bids)


def print_summary(data: dict) -> None:
    """Sanity check — run this first."""
    for name, df in data.items():
        print(f"{name:12s}: {len(df):>6,} rows  |  columns: {list(df.columns)}")


# ─── Step 1: Map RFQ cycle times ──────────────────────────────────────────────
#
# The TOC process starts by understanding the system flow.
# Plot RFQ cycle time (bid_deadline - issue_date) across the 18 months.
# Look for changes in the pattern after September 2024 (month_index >= 8).
#
# Question: Does the cycle time itself change? Or is something else changing?

def plot_rfq_cycle_times(rfq: pd.DataFrame) -> None:
    """
    TODO:
    1. Calculate cycle_days = (bid_deadline - issue_date).dt.days
    2. Group by month_index, compute mean and std of cycle_days
    3. Plot a line chart of mean cycle time over 18 months
    4. Add a vertical line at month_index=8 (September 2024) to mark the tariff shock
    5. Title: "RFQ Cycle Time (Issue → Deadline) — Is this the constraint?"
    """
    # Your code here
    pass


# ─── Step 2: Invited, responding, bidding — three lines, one gap ──────────────
#
# Plot three things per month: how many vendors were INVITED, how many RESPONDED,
# and how many actually BID.
#
# Question: after September 2024, which of these three moves, and which does not?
# One of them is flat for the whole eighteen months. Before you dismiss it, work out
# WHY it is flat — is the thing it measures genuinely healthy, or is this number
# structurally incapable of reporting the damage?
#
# Then ask the question that matters: if procurement reviewed only the flat number
# every month, how long could this problem run before anyone noticed?

def plot_vendor_pool_and_response(rfq: pd.DataFrame, invites: pd.DataFrame,
                                  bids: pd.DataFrame) -> None:
    """
    TODO:
    1. From rfq, plot n_vendors_invited (mean per month_index) — left axis
    2. From invites, plot responders per RFQ per month — left axis, same scale
       (invites.groupby("month_index")["responded"].sum() / RFQs that month)
    3. From bids, plot bids received per RFQ per month — left axis, same scale
       (bids.groupby("month_index").size() / rfq.groupby("month_index").size())
    4. From invites, compute response_rate = responded.mean() per month — right axis
    5. Mark month_index=8 with a vertical line
    6. Title: "Invited vs Actually Bidding — which line is on someone's dashboard?"

    Hint: invites["responded"] is True/False. .sum() counts, .mean() gives the fraction.
    """
    # Your code here
    pass


# ─── Step 3: Trace the root cause — health score trends ───────────────────────
#
# Now look at the four named vendors with distinct arcs:
#   V001  Kovacs Precision GmbH    → declining
#   V003  Patel Alloys Pvt Ltd     → improving
#   V018  Guangzhou Mech & Elec    → collapse
#   V021  Helios Micro Systems     → new_proving
#
# Plot their composite_health_score over 18 months.
# This is the upstream cause of what you saw in Step 2.

FOCUS_VENDORS = {
    "V001": "Kovacs Precision (declining)",
    "V003": "Patel Alloys (improving)",
    "V018": "Guangzhou M&E (collapse)",
    "V021": "Helios Micro (new→proven)",
}

def plot_health_score_arcs(health: pd.DataFrame) -> None:
    """
    TODO:
    1. Filter health for the 4 vendor IDs in FOCUS_VENDORS
    2. Plot composite_health_score vs month for each vendor (4 lines, different colours)
    3. Add a horizontal dashed line at score=80 (the alert threshold — below this + declining = alert)
    4. Mark month_index=8 with a vertical line
    5. Label each line with the vendor name
    6. Title: "Vendor Health Scores — Where Does the Pool Deteriorate?"

    Bonus: shade the region where alert_flag == True for any vendor.
    """
    # Your code here
    pass


# ─── Step 4: Check admin burden — symptom or cause? ──────────────────────────
#
# The procurement team feels exhausted. Is it because of more clarification rounds?
# Or is admin burden a consequence of having fewer healthy vendors?
#
# Plot average clarification_rounds per month. Then compare to the health score chart.
# Which came first?

def plot_admin_burden(burden: pd.DataFrame) -> None:
    """
    TODO:
    1. Filter burden to responded == True (only rows where vendor engaged)
    2. Group by month_index, compute mean clarification_rounds
    3. Plot as a bar chart
    4. Mark month_index=8
    5. Title: "Avg Clarification Rounds per RFQ — Symptom or Constraint?"
    """
    # Your code here
    pass


# ─── Step 5: Name the constraint ─────────────────────────────────────────────

def identify_constraint() -> str:
    """
    TODO: Replace the placeholders with your answers.

    The constraint is not where the pain is loudest. It is the step in the
    procurement pipeline with the least capacity relative to demand.

    Available options (choose one):
      A) RFQ email cycle time (issue to deadline is too short)
      B) Admin burden (too many clarification rounds slow down bids)
      C) Vendor response rate (vendors aren't replying to RFQs)
      D) Vendor pool health (not enough healthy vendors bidding competitively)
    """
    return """
CONSTRAINT: [Your answer: A / B / C / D — and name it in your own words]

EVIDENCE 1: [A specific number from the data — cite something that actually MOVED,\n             not something you expected to move]

EVIDENCE 2: [A second data point that proves it is the root cause, not just a symptom]

CAUSAL CHAIN: [Write the chain: Cause → Effect → Effect → Constraint]
"""


# ─── Step 6: Exploit proposal ────────────────────────────────────────────────

def propose_exploitation() -> str:
    """
    TODO: What could Meridian (or Hermes) do RIGHT NOW — with no new budget —
    to get more throughput from the constrained resource?

    Think about:
    - What information does the system already have that it isn't using?
    - Which vendors are improving and could be given more chances?
    - What actions make the constraint less binding without eliminating it?
    """
    return """
EXPLOIT PROPOSAL: [Your one-paragraph proposal]

EXPECTED IMPACT: [How would this change the charts you drew above?]
"""


# ─── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Loading data...")
    data = load_data()
    print_summary(data)
    print()

    print("Generating charts...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    plt.suptitle("Meridian Procurement — TOC Analysis", fontsize=14, fontweight="bold")

    # TODO: pass axes[0,0], axes[0,1] etc into your plot functions,
    # or call plt.figure() inside each function — your choice.

    plot_rfq_cycle_times(data["rfq"])
    plot_vendor_pool_and_response(data["rfq"], data["invites"], data["bids"])
    plot_health_score_arcs(data["health"])
    plot_admin_burden(data["burden"])

    plt.tight_layout()
    plt.savefig("toc_analysis.png", dpi=150)
    print("Chart saved to toc_analysis.png")
    print()

    print("=== CONSTRAINT IDENTIFICATION ===")
    print(identify_constraint())
    print()

    print("=== EXPLOIT PROPOSAL ===")
    print(propose_exploitation())
