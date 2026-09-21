# Challenge 7 — The Front Door (System 1 Triage) Solution Guide

## Overview
This challenge introduces the architectural concept of separating concerns in AI pipelines: utilizing a fast, cheap **System 1** reflex engine (Laya) to protect and orchestrate a slow, expensive **System 2** reasoning engine (Claude). 

Participants process a messy, multilingual inbox of vendor emails, categorizing and scoring them instantly.

## The Aha! Moments

### 1. The Death of Keywords
In traditional (pre-AI) triage systems, routing was done via keyword regex. If an email contained "invoice," it went to Finance. 

But look at `MSG-003` (the German email) and `MSG-006` (the Japanese email). Unless the user writes regex dictionaries for every language on earth, traditional systems fail. Laya reads the *semantic intent* regardless of language.

### 2. The Power of Ordinal Scoring (`score`)
Look at how the solution defines the urgency criteria:
```python
"criteria": [
    "routine spam or automated notification",
    "general inquiry or minor clarification",
    "moderate delay or warning",
    "significant disruption or price increase",
    "severe threat to partnership, credit hold, or massive supply chain shock"
]
```
Instead of asking an LLM to "generate an urgency score from 1 to 10" (which is notoriously inconsistent and uncalibrated), Laya places the text on an ordinal rubric and calculates a mathematical expected value based on its probability distribution. 

If an email receives a score of `4.2`, it means the engine places high probability on it being a "severe threat."

### 3. The Multilingual Router
In the terminal output, participants should notice:
* English emails are routed using `model: english`.
* The German and Japanese emails are routed using `model: multilingual`.

Because `Router(preload=True)` is used, this switch happens in sub-milliseconds in RAM, rather than incurring a 10-second cold-swap penalty of loading a new model onto the GPU. This is crucial for high-throughput enterprise systems.

## The Pipeline Connection
By the end of this script, `critical_alerts.json` is generated. It only contains the items that scored highly (like the Credit Hold, the Tariff Shock, and the Vendor Consolidation). 

This is the exact payload that should now be sent to **Challenge 3: The Watchdog** or **Challenge 4: The Tactician**. We have successfully built an architecture where System 1 acts as the filter, and System 2 acts as the cognitive planner.