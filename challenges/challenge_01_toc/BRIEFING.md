# Challenge 1: Find the Bottleneck

**Domain:** Theory of Constraints
**Deliverable:** A constraint map with three pieces of data evidence, and a written proposal for what to do next

---

## The Brief

Meridian's head of procurement, Priya Nair, has asked you to explain why the last two quarters have been painful.

"We're sending out RFQs. Vendors are responding. Bids are coming in. So why does it feel like we're always scrambling? Why are our purchase prices up? Why is the team exhausted?"

She's heard of Theory of Constraints and wants you to use it. She specifically said:
*"Don't just tell me what's hurting. Tell me where the system is breaking down. I want one constraint, named with evidence."*

---

## Your Mission

Apply the **TOC 5 Focusing Steps** to Meridian's procurement system.

The 5 steps are:
1. **Identify** the system's constraint
2. **Exploit** it (squeeze maximum throughput from the constraint as-is)
3. **Subordinate** everything else to the constraint
4. **Elevate** the constraint (invest to increase its capacity)
5. **Repeat** (once the constraint shifts, start over)

Your job covers Steps 1 and 2. Steps 3-5 are for the follow-on project.

---

## What to Look For

You are analysing 18 months of data (January 2024 – June 2025). Something changed in late 2024.

The system has several moving parts:
- How many vendors Meridian invites to an RFQ
- How many of those invited vendors actually respond
- How many competitive bids therefore arrive per RFQ
- How many clarification rounds are needed before bids arrive
- How quickly bids come in relative to the deadline
- What quality of bids arrives

**One of these is the constraint. The others are symptoms.**

A common mistake is to look at the most *visible* pain point. The constraint is not always where the noise is loudest.

> **One of the numbers above barely moves across all eighteen months.**
> That is not a bug in the data and it is not a reason to stop looking. When you find
> it, ask three questions: who owns this number, what would have to happen for it to
> change, and would anybody have noticed if the thing it is supposed to measure got
> worse? A metric that cannot move is not evidence of health. It is a blind spot with
> a green light on it.

---

## The Data You Need

| File | What to look at |
|---|---|
| `09_rfq_events.csv` | `bid_deadline` minus `issue_date` (cycle time); `n_vendors_invited` |
| `10_rfq_vendor_invites.csv` | `responded` rate per month, **and responders per RFQ** |
| `12_bids.csv` | **bids received per RFQ per month** — the real measure of competition |
| `22_rfq_admin_burden.csv` | `clarification_rounds` per RFQ per month |
| `23_vendor_health_scores.csv` | `composite_health_score`, `trend_3mo`, `alert_flag` over time |

---

## What to Produce

1. **Three charts** — each answering one question about the system (see `starter.py`)
2. **A constraint statement** — one sentence naming the constraint
3. **Two sentences of evidence** — what in the data proves it
4. **One exploitation proposal** — what Hermes/the procurement team could do *immediately* (without extra budget) to get more throughput from the constraint

---

## A Clue

The generator comment says:

> "Sep 2024 tariff shock → Meridian cash flow stress → late payments → vendor health scores drop → response rates fall → RFQ pool shrinks → Hermes has to work harder → **constraint becomes visible**"

Map that chain in the data. Where does it break down? What's the chokepoint?

---

## Stretch Goal

Once you've named the constraint, look at the `relationship_arc` field on `23_vendor_health_scores.csv`.
Which specific vendors are driving the problem? Name them. What makes them different from stable vendors?
