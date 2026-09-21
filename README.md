# RFQ Agent Workshop — Meridian Industrial Systems Learning Lab

A hands-on workshop using 18 months of synthetic procurement data from a realistic manufacturing company. You will investigate what went wrong at Meridian in late 2024, quantify the business impact, and build AI agents to prevent future crises.

---

## The Scenario

**Meridian Industrial Systems** manufactures CNC machines and robotic assembly cells. In late 2024, deliveries slipped, costs crept up, and the procurement team felt exhausted — but nobody could name the root cause.

Your job: diagnose the problem using 18 months of data, then build AI agents to solve it.

**The causal chain (spoilers minimized):** A September 2024 tariff shock triggered a cascade through Meridian's supply chain. The workshop gives you the data; your job is to trace the chain and quantify the damage.

---

## Structure

```
RFQ_Agent_Workshop/
├── challenges/                     # 4 independent coding challenges
│   ├── README.md                   # Briefing for all challenges
│   ├── challenge_01_toc/           # Theory of Constraints analysis
│   ├── challenge_02_throughput/    # Throughput Accounting model
│   ├── challenge_03_agent_watchdog/  # Monitoring agent (Claude-powered)
│   └── challenge_04_agent_tactician/ # Planning agent (Claude-powered)
├── output_v2/                      # Synthetic dataset (23 CSV files, 18 months)
├── skills/                         # Pre-built Claude skills (.zip)
├── demo/                           # RFQ pipeline HTML visualizations
├── solutions/                      # Reference solution PDFs (Challenge 01–04)
└── Setup Guide.pdf                 # Environment setup instructions
```

---

## Prerequisites

**Python 3.8+** with the following packages:

```bash
pip install pandas matplotlib anthropic
```

**Challenges 3 and 4 require an Anthropic API key:**

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Challenges 1 and 2 are fully standalone — no API key needed.

---

## The Four Challenges

Each challenge is **fully independent**. Do them in any order, skip any one, or run them in parallel as a group exercise.

| # | Title | Domain | Beginner | Experienced |
|---|-------|--------|----------|-------------|
| 1 | Find the Bottleneck | Theory of Constraints | 90 min | 45 min |
| 2 | What's It Worth? | Throughput Accounting | 90 min | 45 min |
| 3 | The Watchdog | Agentic AI — Monitoring | 2 hrs | 75 min |
| 4 | The Tactician | Agentic AI — Planning | 2.5 hrs | 90 min |
| 6 | The Oracle | Zero-Shot Forecasting (TimesFM) | 90 min | 45 min |
| 7 | The Front Door | System 1 Triage (Laya) | 60 min | 30 min |

---

### Challenge 1 — Find the Bottleneck

**Theory of Constraints analysis.**

Analyze 18 months of RFQ data to identify the system constraint. Produce four charts:

1. RFQ cycle time trends (issue date → bid deadline)
2. Invited vs. responding vs. bidding vendors per month
3. Vendor health score arcs for four focus vendors
4. Admin burden (clarification rounds) per RFQ

Then name the constraint in one sentence, provide two data points as evidence, and propose an exploitation strategy that requires no budget.

**Deliverables:** 4 charts (PNG), constraint statement, evidence, exploitation proposal

---

### Challenge 2 — What's It Worth?

**Throughput Accounting financial model.**

Build a monthly TA model comparing the pre-constraint period (Jan–Aug 2024) against the constraint period (Sep 2024–Jun 2025):

- **T (Throughput)** = Revenue − TVC (material cost)
- **I (Investment)** = Cash tied up in payment cycles
- **OE (Operating Expense)** = Incremental admin cost from the constraint

Quantify total Throughput lost and calculate the breakeven spend on vendor health remediation.

**Assumptions provided in the briefing:** $150 per clarification round (1.5 hrs @ $100/hr), 0.8%/month inventory holding cost.

**Deliverables:** `ta_model.csv`, `ta_summary.csv`, `ta_charts.png`, breakeven statement

---

### Challenge 3 — The Watchdog

**Claude-powered vendor monitoring agent.**

Build an agent that ingests vendor health data monthly and surfaces structured alerts. The agent has five tools to query:

| Tool | Returns |
|------|---------|
| `get_health_snapshot(month_index)` | All vendors' composite scores |
| `get_vendor_trend(vendor_id, n_months)` | Historical trend |
| `get_payment_history(vendor_id, n_months)` | Meridian's payment behavior |
| `get_dispute_history(vendor_id)` | Delivery/quality disputes |
| `get_rfq_participation(vendor_id, n_months)` | Bid and win rates |

The agent decides which tools to call and in what order. For each at-risk vendor it produces a structured alert:

```json
{
  "vendor_id": "V001",
  "alert_severity": "HIGH",
  "composite_score": 73.8,
  "trend": "declining",
  "root_cause": "...",
  "supporting_evidence": [...],
  "recommended_action": "...",
  "urgency": "act_this_month"
}
```

**Deliverables:** Agent code, alerts JSON, monthly alert report

---

### Challenge 4 — The Tactician

**Claude-powered RFQ planning agent.**

Build an agent that receives a Work Order and produces an optimized RFQ plan. The agent has seven tools, including market signals, commodity prices, competitor activity, and vendor health queries. It must adapt strategy based on conditions — not just fetch data.

Run the agent for three different months to compare behavior:

| Month | Conditions |
|-------|-----------|
| 5 (Jun 2024) | Pool healthy — standard playbook |
| 10 (Nov 2024) | Constraint active — pool degraded, must adapt |
| 15 (Apr 2025) | Partial recovery — rare earth price shock |

**Stretch goal:** "What-if" mode — re-plan with a vendor removed, budget cut 15%, or urgency changed.

**Deliverables:** Agent code, RFQ plans JSON, 3-month comparison analysis

---

### Challenge 6 — The Oracle

**Zero-Shot Time Series Forecasting with Google TimesFM.**

Move Meridian from a reactive to a predictive posture. In this challenge, you will use Google's TimesFM to forecast supply chain bottlenecks and commodity prices without training a model.

1. **Market Shock Anomaly Detection:** Feed historical "Rare Earth Element" prices into TimesFM. Write logic to trigger an alert when actual prices breach the model's 95% confidence bounds, predicting the April 2025 crisis before it devastates the budget.
2. **Lead Time Forecasting:** Forecast the system's cycle times before the tariff shock. Analyze the divergence between univariate statistical forecasting and exogenous causal events.

**Deliverables:** `oracle.py` implementation, anomaly JSON payload, and forecast visualization charts.

---

### Challenge 7 — The Front Door

**System 1 High-Volume Triage with Laya.**

Meridian's procurement inbox is flooded with thousands of emails across multiple languages. Using a slow System 2 LLM (like Claude) for routing is too expensive and hits rate limits.

In this challenge, you will deploy **Laya**, a sub-35ms System 1 reflex engine, to act as the "Front Door".
1. **Semantic Queue Assignment:** Route complex emails to Engineering, Logistics, Finance, etc., without relying on keyword matching.
2. **Panic Meter:** Use ordinal scoring to calculate a calibrated urgency score for each email.
3. **Multilingual Native Routing:** Seamlessly process German and Japanese supply chain warnings in milliseconds without calling translation APIs.

Filter the output to pass *only* the critical alerts to the System 2 agents.

**Deliverables:** `triage.py` implementation, `critical_alerts.json` output payload.

---

## Dataset

23 CSV files in `output_v2/` covering January 2024 through June 2025 (`month_index` 0–17).

| File | Description |
|------|-------------|
| `01_vendors.csv` | 24 vendors — archetypes, categories, risk tiers |
| `02_vendor_performance.csv` | Monthly KPI snapshots |
| `03_commodity_prices.csv` | Weekly prices + shock flags |
| `04_market_signals.csv` | Tariffs, capacity announcements |
| `05_sales_orders.csv` | Customer orders and revenue |
| `07_work_orders.csv` | Internal work orders (RFQ basis) |
| `09_rfq_events.csv` | RFQ issuance, deadlines, cycle times |
| `10_rfq_vendor_invites.csv` | Invitations sent; response status |
| `12_bids.csv` | Bid prices and delivery commitments |
| `13_bid_evaluation.csv` | Scored and ranked bids |
| `14_purchase_orders.csv` | Winning bids → POs |
| `16_vendor_disputes.csv` | Late delivery and quality disputes |
| `20_payment_events.csv` | Meridian's payment events |
| `22_rfq_admin_burden.csv` | Clarification rounds per RFQ |
| `23_vendor_health_scores.csv` | Monthly composite health + alerts |
| `24_event_log.csv` | Complete event timeline |

---

## How to Work Each Challenge

1. **Read `BRIEFING.md`** before touching code.
2. **Open `starter.py`** and read the full file including all TODOs.
3. **Run `starter.py` as-is** — it loads data and prints shapes as a sanity check.
4. **Work through TODOs in order** — earlier steps inform later ones.
5. **Write conclusions in prose** — explain the *why*, not just the numbers.

The data has surprises. Things that look like the constraint are often symptoms. Trust the numbers over intuitions.

---

## Technology Stack

- **Python 3.8+**
- **pandas** — data manipulation
- **matplotlib** — charting
- **anthropic SDK** — Claude API (Challenges 3 and 4)
- **Claude API** — tool use and agentic reasoning patterns

---

## Included Resources

- **`Setup Guide.pdf`** — environment setup and API key configuration
- **`solutions/`** — reference solution PDFs for all four challenges
- **`skills/`** — 9 pre-built Claude skills for agent development (zipped)
- **`demo/`** — HTML visualizations of the RFQ pipeline and data schema
