# Challenge 4: The Tactician

**Domain:** Agentic AI — Planning and Optimisation Pattern
**Deliverable:** A working Python agent that receives a Work Order and produces an optimised RFQ vendor selection plan

---

## The Brief

A new Work Order just landed. Priya's team needs to issue an RFQ in the next 24 hours.

But the system is under strain:
- The Watchdog flagged 4 vendors as unhealthy this month
- Copper prices spiked last week (relevant for Electrical Components RFQs)
- The competitor Hexagon AG is also running RFQs right now, competing for the same vendor capacity

The standard playbook: invite 8 vendors, wait for bids, pick the top 5.
That's not going to work when the pool has problems. Someone — or something — needs to think.

The Tactician agent takes a Work Order ID, reads the situation, makes a plan, and outputs an actionable RFQ strategy. It doesn't just report the problem — it decides what to do.

---

## Agent Pattern: The Deliberate Planner

This challenge teaches the **planning agent** pattern:

```
Goal (new Work Order arrives)
  → Assess (what do I know about this category's vendors and market?)
    → Plan (which vendors to invite, in what priority, with what terms?)
      → Adapt (what if fewer than 8 healthy vendors are available?)
        → Execute (output the RFQ plan as structured data)
```

The key difference from the Watchdog: the Tactician has a **goal it must achieve**
(a viable RFQ), and it must **adapt its plan** when the situation is unfavorable.

This is the core of agentic reasoning: goal-directed, adaptive, multi-step planning.

---

## The Shape of the Agent

```
agent_tactician(work_order_id: str, month_index: int) -> RFQPlan

Tools available:
  get_work_order(work_order_id)             → WO details, category, budget
  get_vendor_pool(category)                 → all vendors in this category
  get_vendor_health(vendor_id, month_index) → current health score + trend
  get_market_signals(category)              → recent signals for this category
  get_commodity_prices(category, weeks)     → recent price data
  get_competitor_activity(month_index)      → Hexagon AG capacity competition signal
  create_rfq_plan(...)                      → finalise and return the plan (output tool)
```

---

## RFQ Plan Structure

```python
{
    "work_order_id": "WO-2024-0187",
    "category": "Electrical Components",
    "urgency": "expedited",
    "budget_ceiling_usd": 142500,

    "vendor_shortlist": [
        {
            "vendor_id": "V002",
            "vendor_name": "Tanaka Electrical KK",
            "health_score": 78.4,
            "invite_priority": 1,
            "rationale": "..."
        },
        ...
    ],

    "n_vendors_to_invite": 8,     # may be less if pool is constrained
    "rfq_terms": {
        "bid_window_days": 7,
        "evaluation_weights": {"price": 0.4, "delivery": 0.3, "quality": 0.2, "relationship": 0.1},
        "special_conditions": "..."
    },

    "market_context": "...",       # key market factors affecting this RFQ
    "risk_flags": [...],           # notable risks in this RFQ
    "adaptation_notes": "..."      # what the agent changed from the standard playbook
}
```

---

## The Interesting Agentic Decisions

The Tactician must make real decisions, not just rank vendors:

1. **Pool shortfall**: If only 5 healthy vendors exist for this category, what should
   the agent do? Invite unhealthy ones? Expand to adjacent categories? Recommend delay?

2. **Market timing**: A commodity price spike means bids will come in high. Should the
   agent adjust the budget ceiling signal in the RFQ? Adjust evaluation weights?

3. **Competitor pressure**: If Hexagon AG is also buying in this category this month,
   vendor capacity is tighter. Should the agent widen the bid window to attract more responses?

4. **Urgency tradeoffs**: A "critical" urgency WO with a bad vendor pool — does the agent
   recommend proceeding with fewer vendors (faster) or flagging to management for intervention?

5. **Arc awareness**: The agent should prefer improving-trend vendors over stable ones,
   and deprioritise collapse-arc vendors even if their scores aren't critically low yet.

---

## What to Build

Complete the TODO sections in `starter.py`. The tools are implemented.
Your job is to write:
1. The system prompt that makes the agent a genuine strategic thinker
2. The agentic loop (same structure as Challenge 3, but goal-oriented)
3. Logic to extract the structured RFQ plan from the agent's response

---

## Challenge Twist

Run the agent for:
- Month 5 (June 2024) — before the constraint bites. Pool is healthy.
- Month 10 (November 2024) — constraint is active. Pool is degraded.
- Month 15 (April 2025) — late-period. Some recovery, but rare earth shock.

Compare the three plans. Does the agent's strategy change appropriately?
What does it do when the situation gets hard?

---

## Stretch Goal

After the agent generates the plan, add a **"what-if" mode**:
- What if Kovacs (V001) were removed from the pool entirely?
- What if the budget were cut by 15%?
- What if urgency changed from standard to critical?

The agent should re-plan from the same starting point with the new constraint.
This tests whether your agent truly adapts or is just following a fixed script.
