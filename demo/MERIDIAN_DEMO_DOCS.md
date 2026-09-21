# Meridian Industrial Systems: AI Triage & Routing Demo
 
 This document outlines four specialized demonstration scenarios for the **Laya AI Routing Engine**, specifically adapted to the lore and data of the **Meridian Industrial Systems RFQ Workshop**. These scenarios demonstrate Laya's ability to triage and route complex supply chain, procurement, and vendor communications.
 
 ## Overview
 Meridian Industrial Systems manufactures CNC machines and robotic cells. In late 2024, a major tariff shock triggered a supply chain crisis. The routing engine is deployed to prevent future crises by intelligently triaging internal and external communications.
 
 This demo suite proves that the routing engine can simultaneously evaluate:
 1. **Cross-Departmental Routing** (Procurement, Engineering, Finance, Logistics)
 2. **Supply Chain Urgency** (Scoring bottlenecks and constraint starvation)
 3. **Hidden Risks** (Vendor flight risk, compliance breaches, financial impacts)
 4. **Global Sourcing** (Handling multilingual vendor emails and massive data payloads)
 
 ---
 
 ## Prerequisites
 1. **Python 3.8+** is installed.
 2. The **`laya`** package is installed and accessible in your current virtual environment.
 3. Execute scripts from the directory containing them (`/home/happyveggie/Projects/laya/`).
 
 *Note: The scripts contain a fallback mechanism. If `laya` is not found, they execute a "Dry Run" mode.*
 
 ---
 
 ## 📂 Scenario 1: Complex Supply Chain Disruptions
 **File:** `demo_01_meridian_incidents.py`
 
 **The Business Value:** Supply chain issues often cross departmental boundaries. A delayed shipment (Logistics) starves a CNC assembly cell (Operations), creating a throughput bottleneck (Finance). Laya identifies the primary owner of the issue.
 
 **Highlighted Tests:**
 *   **Throughput Impact:** Idle assembly cells causing massive financial loss.
 *   **Admin Burden:** Vendors threatening to withdraw due to excessive engineering clarification rounds.
 *   **WIP Accumulation:** Investment tied up in front of a system constraint.
 
 ---
 
 ## 📂 Scenario 2: Vendor Health & Supply Churn
 **File:** `demo_02_meridian_vendor_risk.py`
 
 **The Business Value:** Vendors rarely scream when they drop you; they subtly extend lead times, pass on bids, or mention capacity limits. This script demonstrates detecting hidden `supplier_flight_risk` to save critical supplier relationships before they break.
 
 **Highlighted Tests:**
 *   **Capacity Constraints:** Vendors passing on RFQs due to late payment cycles.
 *   **Lead Time Extensions:** Sudden jumps in raw material procurement times.
 *   **Credit Holds:** Account freezes due to past-due invoices.
 
 ---
 
 ## 📂 Scenario 3: Tariff Shocks & Trade Compliance
 **File:** `demo_03_meridian_compliance.py`
 
 **The Business Value:** Missing a market signal or compliance violation (like ITAR) can cost millions. This scenario triggers on legal holds, exposed confidential pricing, and market shocks.
 
 **Highlighted Tests:**
 *   **The Q3 Tariff Shock:** Ingesting intelligence about sudden tariffs on electronics.
 *   **ITAR Violations:** Accidental sharing of unredacted defense blueprints to foreign suppliers.
 *   **Data Leaks:** Vendor pricing matrices exposed in public cloud buckets.
 
 ---
 
 ## 📂 Scenario 4: Global Sourcing & Multilingual RFQs
 **File:** `demo_04_meridian_localization.py`
 
 **The Business Value:** Meridian buys from suppliers worldwide. This script proves the model can natively categorize non-English emails and handle massive data stress.
 
 **Highlighted Tests:**
 *   **Multilingual Triage:** Parsing delay notices and clarification requests in Japanese, German, Spanish, and French.
 *   **Data Stress:** Handling a massive JSON payload failure from legacy RFQ systems.
 
 ---
 
 ## 🚀 How to Run the Demos
 
 Open your terminal, navigate to your project directory, and execute the scripts directly using Python:
 
 ```bash
 cd /home/happyveggie/Projects/laya/
 
 python demo_01_meridian_incidents.py
 python demo_02_meridian_vendor_risk.py
 python demo_03_meridian_compliance.py
 python demo_04_meridian_localization.py
 ```
 
 ---
 
 ## 📖 Laya Engine Under the Hood
 
 The Meridian demonstration scenarios are powered by **Laya**, a 33ms Multilingual System 1 Decision Engine with Calibrated Probabilities.
 
 ### Why Laya for Triage?
 Every modern AI pipeline using generative LLMs (System 2) faces a bottleneck when answering simple, structured questions (e.g., ticket routing, urgency scoring, threat detection). LLMs introduce massive latency (500-2,000ms) and fake confidence. Laya acts as a **System 1** reflex engine, processing inputs in 32.8 milliseconds on a single GPU with mathematical calibration. 
 
 ### Core Decision Primitives
 Laya evaluates typed questions over any state in a single forward pass utilizing these primitives:
 1. **choice**: Picks an option from a dictionary of criteria, yielding the selected key, probability distribution, and a calibrated confidence score.
 2. **score**: Places the input on an ordinal rubric, returning an expected level and distribution over rubric ranks.
 3. **noul**: Evaluates a direct boolean question returning a calibrated probability P(true) from 0.0 to 1.0.
 
 By outputting purely probabilities and numbers, the model never generates text, completely eliminating hallucinations and schema violations.
 
 ### Built-in Multi-Script Routing
 To effectively support global sourcing, English-only models degrade sharply on non-Latin scripts, maintaining false high confidence. Laya solves this using a built-in sub-millisecond `Router` that analyzes text across 22 alphabets and intelligently directs payloads to the appropriate multilingual model (like `mmBERT-base` covering 100+ languages).
 
 ---
 
 ## 🙏 Credits
 
 **Laya** was created and open-sourced by **Nandakishor Mukkunnoth**, Founder & CEO of **ConvAI Innovations**. 
 
 By formalizing the framework for schema-based decisions guided by reinforcement learning (RLCD), Laya provides a breakthrough 100% open-source alternative for high-volume enterprise classification and routing.
 
 Learn more, read the research, and access the open weights at the official site:  
 **[Laya - ConvAI Innovations](https://laya.convaiinnovations.com/)**
