# Challenge 2: What's It Worth?

**Domain:** Throughput Accounting
**Deliverable:** A Throughput Accounting model (CSV output) showing the $ value of Meridian's vendor health problem

---

## The Brief

Priya Nair now knows the constraint (you found it in Challenge 1).

But the CFO, Arjun Desai, isn't convinced it needs fixing. His position:
*"Procurement feels slow, yes. But our costs haven't exploded. If we invest in fixing vendor relationships — outreach, early payments, forecast sharing — that's real money. Show me the business case."*

He's asked for the analysis in Throughput Accounting terms, not traditional cost accounting.

---

## Throughput Accounting Primer

Traditional accounting asks: "What does this cost?"
Throughput Accounting asks: "What does this constraint do to our ability to make money?"

The three measures:

| Measure | Definition | In this context |
|---|---|---|
| **T — Throughput** | Revenue minus Truly Variable Costs | SO revenue minus PO material spend |
| **I — Investment** | Money tied up in the system | Cash tied up in vendor payment cycles |
| **OE — Operating Expense** | All other fixed costs | Admin time in procurement (clarification rounds, chasing bids) |

The key metric is **Net Profit = T - OE** and **ROI = (T - OE) / I**

The vendor health constraint affects all three:
- **T drops** because fewer competitive bids → higher purchase prices → narrower margin
- **I increases** because payment disputes and delays tie up cash longer
- **OE rises** because more clarification rounds → more procurement team hours

---

## Your Mission

Build a monthly Throughput Accounting model that shows:

1. **T, I, and OE** for each month (months 0-17)
2. A **before/after comparison**: months 0-7 (Jan-Aug 2024) vs months 8-17 (Sep 2024 - Jun 2025)
3. The **total T lost** due to the constraint period
4. The **breakeven investment** — how much could Meridian afford to spend fixing vendor health?

---

## Key Insight to Find

The pain is NOT in operating expense. Clarification rounds add friction, but the team's salaries are fixed — OE barely moves.

The real damage is in **T**: when the vendor pool shrinks, competitive pressure drops, and Meridian pays more for the same materials. Higher TVC = lower T.

---

## The Data You Need

| File | What to extract |
|---|---|
| `05_sales_orders.csv` | `total_value_usd` per month — this is Revenue |
| `14_purchase_orders.csv` | `po_value_usd` per month — this is Truly Variable Cost (TVC) |
| `20_payment_events.csv` | `days_late` × `po_value_usd` — proxy for Investment tied up |
| `22_rfq_admin_burden.csv` | `clarification_rounds` × cost rate — proxy for OE friction |
| `12_bids.csv` | `bid_total_usd` and `bid_unit_price` — spot the price creep |

---

## Assumptions to Use

These are intentionally simplified so you can focus on the model structure:

- **OE per clarification round**: $150 (1.5 hours of procurement team time at $100/hr)
- **Inventory holding cost**: 0.8% per month of outstanding PO value (cash opportunity cost)
- **Revenue per SO**: use `total_value_usd` directly (Meridian earns full invoice)
- **TVC**: use PO spend (`po_value_usd`) as the only truly variable cost

---

## What to Produce

1. A **monthly TA table** (save as `ta_model.csv`) with columns:
   - `month_index`, `revenue_usd`, `tvc_usd`, `throughput_usd`
   - `investment_tied_up_usd`, `oe_friction_usd`
   - `net_profit_proxy`, `roi_proxy`

2. A **summary table** comparing pre-constraint vs post-constraint periods

3. A **single number**: the total T lost in the constraint period vs the pre-constraint run rate

4. A **breakeven statement**: "Meridian could spend up to $X fixing vendor health and still be ahead"

---

## What NOT to Do

- Do not use cost accounting logic (allocating overhead, calculating unit margins)
- Do not treat OE as variable — the team is on salary whether they answer 1 or 10 clarification rounds
- Do not add depreciation, R&D, or any non-TVC costs to the TVC calculation

---

## Stretch Goal

Plot the **bid price spread** (max bid minus min bid per RFQ, by month).
When the vendor pool shrinks, does the spread narrow? What does a narrow spread mean for T?

Hint: if only 3 vendors bid instead of 7, competitive pressure drops — even if the cheapest bid
price is similar, Meridian has less negotiating leverage.
