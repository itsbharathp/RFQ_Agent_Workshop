# Meridian Industrial Systems — Learning Lab

A hands-on workshop using 18 months of synthetic procurement data from a real-world-shaped company.

---

## The Scenario

**Meridian Industrial Systems** makes CNC machines and robotic assembly cells.
Their procurement team runs Request-for-Quotation (RFQ) cycles to source components.
Something went wrong in late 2024. Deliveries slipped, costs crept up, and the team felt stretched thin — but nobody could name the problem.

Your job: figure out what broke, quantify the damage, and build the AI agents that should have caught it.

---

## The Data

All challenges read from the `output_v2/` directory (one level up). 23 CSV files covering:

| File | Contents |
|---|---|
| `01_vendors.csv` | 24 vendors — categories, archetypes, risk tiers |
| `02_vendor_performance.csv` | Monthly KPI snapshots per vendor |
| `05_sales_orders.csv` | Customer orders with value and deadline |
| `09_rfq_events.csv` | One row per RFQ issued |
| `10_rfq_vendor_invites.csv` | Who was invited to each RFQ, did they respond? |
| `12_bids.csv` | Bid prices and delivery commitments |
| `13_bid_evaluation.csv` | Scored and ranked bids |
| `14_purchase_orders.csv` | Winning bids converted to POs |
| `20_payment_events.csv` | When Meridian actually paid vendors |
| `22_rfq_admin_burden.csv` | Clarification rounds, spec quality per RFQ |
| `23_vendor_health_scores.csv` | Monthly relationship health (composite score + trend) |

---

## The Four Challenges

| # | Title | Domain | Output |
|---|---|---|---|
| 1 | **Find the Bottleneck** | Theory of Constraints | Constraint map + evidence |
| 2 | **What's It Worth?** | Throughput Accounting | TA model with $ impact |
| 3 | **The Watchdog** | Agentic AI — Monitoring | Alert-generating agent |
| 4 | **The Tactician** | Agentic AI — Planning | RFQ planning agent |

Each challenge is fully independent. Do them in any order.

---

## Prerequisites

```bash
pip install pandas matplotlib anthropic
```

For Challenges 3 and 4, you need an Anthropic API key:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

---

## Time Estimates

| Challenge | Beginner | Experienced |
|---|---|---|
| 1 — TOC | 90 min | 45 min |
| 2 — Throughput Accounting | 90 min | 45 min |
| 3 — Watchdog Agent | 2 hrs | 75 min |
| 4 — Tactician Agent | 2.5 hrs | 90 min |

---

## How to Approach Each Challenge

1. Read the `BRIEFING.md` — understand the mission before touching code
2. Open `starter.py` — read the whole file before filling in any TODO
3. Run the starter as-is first (it loads data and prints shapes)
4. Work through the TODOs in order — earlier steps inform later ones
5. Write your conclusion in prose, not just numbers

The data has surprises. Some things that look like the constraint are symptoms.
Trust the numbers over your intuitions.
