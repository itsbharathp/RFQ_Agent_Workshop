# Challenge 3: The Watchdog

**Domain:** Agentic AI — Monitoring and Detection Pattern
**Deliverable:** A working Python agent that detects at-risk vendors and generates structured alerts

---

## The Brief

Meridian was blindsided. Vendor health deteriorated for months before the RFQ pool shrank.
The data was there — it just wasn't being watched.

Priya Nair wants an AI agent that monitors vendor health monthly and fires an alert
*before* a vendor becomes unusable. Not a dashboard. Not a report. An **agent** — something
that actively reasons about the data and decides what warrants attention and what doesn't.

The key difference from a rule-based alert system: the agent should explain **why** it's
alerting, not just **that** the threshold was crossed. It needs to:
- Look at trends, not just point-in-time scores
- Cross-reference payment history and dispute patterns
- Produce a root-cause hypothesis
- Recommend a specific action

---

## Agent Pattern: The Sensor-to-Alert Loop

This challenge teaches the **monitoring agent** pattern:

```
Observe (read current state)
  → Analyse (reason about what it means)
    → Classify (is this urgent? why?)
      → Recommend (what to do)
        → Alert (structured output)
```

This is a **tool-using agent**: it has tools to query different data tables,
and it decides which tools to call and in what order based on what it discovers.

---

## The Shape of the Agent

```
agent_watchdog(month_index: int) -> list[Alert]

Tools available:
  get_health_snapshot(month_index)         → all vendors' scores for this month
  get_vendor_trend(vendor_id, n_months)    → score history for a vendor
  get_payment_history(vendor_id, n_months) → payment events for a vendor
  get_dispute_history(vendor_id)           → open disputes for a vendor
  get_rfq_participation(vendor_id, n_months) → invite/response/win history
```

The agent is given the current month. It should:
1. Fetch the health snapshot to find vendors below threshold or with declining trends
2. For each at-risk vendor, fetch deeper context (trend, payments, disputes, RFQ history)
3. Reason about the root cause
4. Generate an Alert for each vendor that warrants attention

---

## Alert Structure

Each alert should contain:

```python
{
    "vendor_id": "V001",
    "vendor_name": "Kovacs Precision GmbH",
    "alert_severity": "HIGH",          # LOW / MEDIUM / HIGH / CRITICAL
    "composite_score": 73.8,
    "trend": "declining",
    "root_cause": "...",               # Agent's hypothesis
    "supporting_evidence": [...],      # List of specific data points
    "recommended_action": "...",       # Specific, actionable recommendation
    "urgency": "act_this_month"        # act_this_month / monitor / watch
}
```

---

## The Interesting Agentic Decisions

The agent must make non-trivial choices:

1. **Score threshold vs trend**: A vendor at 62 with a declining trend may be more
   concerning than a vendor at 55 who has been stable there for months.

2. **Root cause triage**: Is the vendor declining because Meridian is paying them late?
   Or because they are genuinely struggling? The agent should check both directions.

3. **New vendors**: A thin-data-flag vendor (new_proving arc) with a low score is
   *expected* to have low scores early — the agent should not over-alert on them.

4. **Improving vendors**: Should the agent also alert on positive trends?
   (A vendor improving fast might deserve a relationship investment recommendation.)

---

## What to Build

Complete the TODO sections in `starter.py`. The tools are fully implemented.
Your job is to write:
1. The main agent loop (calling tools, reasoning, deciding what to investigate)
2. The system prompt for the Claude agent
3. The alert generation logic

---

## What Makes a Good Agent vs a Bad One

**Bad:** Alerts on every vendor below 70. Copy-pastes the data without synthesis.

**Good:** Alerts only on vendors where the data tells a coherent story. Explains
the *mechanism* of deterioration. Recommends something *specific*, not "monitor closely".

---

## Stretch Goal

Add a `positive_alerts` mode: surface vendors that are *improving faster than expected*
and recommend proactive actions (e.g., "Patel Alloys is trending up 8 points in 3 months —
consider offering a forecast sharing arrangement to lock in this relationship").

The best alert systems catch both risks AND opportunities.
