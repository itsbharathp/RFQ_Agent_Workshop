# Challenge 7 — The Front Door (System 1 Triage)

## Context
As the tariff shock of late 2024 ripples through the supply chain, Meridian's shared procurement inbox (`vendors@meridian.com`) is completely overwhelmed. Vendors are sending thousands of emails: routine invoices, shipping delays, furious threats of cancellation, technical engineering questions, and outright spam.

Currently, Meridian is attempting to use the newly developed "Watchdog" agent (Claude/System 2) to read every single email. It takes 3 seconds per email, costs hundreds of dollars a day in API fees, and frequently hits rate limits.

The CIO demands a "Front Door"—a System 1 reflex engine.

## The Tool: Laya
You must deploy **Laya** (a sub-35ms open-weight System 1 decision engine) to instantly process, route, and score the urgency of incoming communications. It must pass *only* the critical, high-risk items to the System 2 Watchdog.

Laya utilizes three primitives for decision making:
1. `choice`: Pick one option from a predefined dictionary of criteria.
2. `score`: Place the state on an ordinal rubric (e.g., levels 0 to 5).
3. `noul`: A direct boolean question returning a calibrated probability.

Laya also features a built-in multi-lingual `Router` that can handle global communications natively.

---

## Objectives

### Task 1: Semantic Queue Assignment (`choice`)
Configure a `choice` question in Laya to categorize each incoming email into one of the following queues based on its semantic meaning (not just keyword matching):
*   `engineering`
*   `logistics`
*   `finance`
*   `procurement`
*   `spam`

### Task 2: The Panic Meter (`score`)
Configure a `score` question on a 0 to 5 ordinal rubric to gauge vendor panic/urgency. You need to differentiate between a routine update (low score) and a severe threat like an account credit hold or a sudden price shock (high score).

### Task 3: Execute Multilingual Routing
Initialize `laya.Router(preload=True)`. Pass the provided `vendor_inbox.json` through the Laya engine. Ensure that the engine successfully reads and triages the German and Japanese emails without you having to write any translation logic.

### Task 4: Filter Critical Alerts
Parse the results from Laya. Extract only the emails that received an urgency score of **4.0 or higher** and save them to `critical_alerts.json`.

---

## Deliverables
1. `triage.py`: Your completed script based on `starter.py`.
2. `critical_alerts.json`: The filtered output containing the high-urgency emails.

---

## Getting Started
Ensure you have installed the required dependencies:
```bash
pip install laya>=0.3.3
```