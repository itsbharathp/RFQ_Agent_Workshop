import json
import time
try:
    from laya import Router
    router = Router(preload=True)
except ImportError:
    print("Warning: laya module not found. Please run within the laya environment.")
    router = None

# Complex Supply Chain Disruptions
# These messages represent cross-functional bottlenecks impacting Meridian Industrial Systems.

tickets = [
    {
        "ticket_id": "RFQ-EVT-101", "sender": "Logistics_Sub_A",
        "subject": "Delay in Aluminum Stock - Throughput Impacted",
        "body": "The recent tariff shock on aluminum imports has caused our shipments to be held at the port. This will delay the raw material for Work Order WO-992 by at least 14 days. We need Procurement to approve the expedited air freight cost or Engineering to sign off on a domestic alloy substitute."
    },
    {
        "ticket_id": "RFQ-EVT-102", "sender": "Internal_Assembly_Floor",
        "subject": "CNC Cell 4 Starved - Missing Actuators",
        "body": "Assembly cell 4 is currently idle. We cannot proceed with the robotic arm assembly because the precision actuators from Vendor V012 are late. This is becoming our primary system constraint. Finance needs to know we are missing this month's throughput target by $400k if this isn't resolved."
    },
    {
        "ticket_id": "RFQ-EVT-103", "sender": "Finance_AP",
        "subject": "Payment Hold on RFQ-8832 Deliverable",
        "body": "We are holding the $85,000 payment for RFQ-8832. The delivered goods failed the Quality Assurance tolerance check (dispute logged). However, the vendor is threatening to halt all future shipments until this is paid. Procurement needs to mediate immediately."
    },
    {
        "ticket_id": "RFQ-EVT-104", "sender": "Vendor_Nexus_Machining",
        "subject": "Clarification Overload on Spindle Specs",
        "body": "Your engineering team has issued 4 separate clarification rounds for the spindle housing Work Order. This administrative burden is too high for our estimating team. We are withdrawing our bid for this RFQ unless we get a single, consolidated blueprint today."
    },
    {
        "ticket_id": "RFQ-EVT-105", "sender": "Production_Manager",
        "subject": "WIP Inventory Accumulating at Constraint",
        "body": "We have $2.5M of Investment (WIP inventory) piled up in front of the final QA testing station. The testing equipment calibration is out of spec, and we need the OEM to send a technician. Escalating to Engineering and Operations—this is destroying our cycle time."
    }
]

questions = {
    "department": {
        "type": "choice",
        "instructions": "Which Meridian department is the primary owner of resolving this issue?",
        "criteria": {
            "procurement": "vendor mediation, expediting materials, managing RFQ bids, tariffs",
            "engineering": "blueprint clarifications, QA tolerance, alternative materials, technical specs",
            "finance": "invoices, payments, throughput impact, holding costs",
            "operations": "assembly floor, WIP inventory, internal bottlenecks"
        }
    },
    "bottleneck_risk": {
        "type": "score",
        "instructions": "How severely does this threaten Meridian's primary system constraint or throughput?",
        "criteria": ["no throughput impact", "minor delay", "major constraint starvation", "critical throughput blocker"]
    },
    "financial_impact": {
        "type": "noul",
        "instructions": "Does the message mention specific dollar amounts, lost revenue, or severe financial consequences?"
    }
}

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 DEMO: SCENARIO 1 - COMPLEX SUPPLY CHAIN DISRUPTIONS (MERIDIAN)")
    print("="*70 + "\n")
    
    for t in tickets:
        print(f"🎫 TICKET: {t['ticket_id']} | SENDER: {t['sender']}")
        print(f"📌 SUBJECT: {t['subject']}")
        
        if router:
            res = router.predict(t, questions)
            print(f"   [Routing] Model: {res.get('routing', {}).get('model', 'N/A')}")
            print(f"   [Department] Assigned: {res['answers']['department']['choice']}")
            print(f"   [Constraint Risk] Score: {res['answers']['bottleneck_risk']['score']:.2f}")
            financial = res['answers']['financial_impact'].get('noul', 0)
            print(f"   [Financial Impact] Likelihood: {financial:.1%}")
        else:
            print("   [Dry Run] Model evaluation skipped (laya not loaded).")
        print("-" * 70)
        time.sleep(0.5)
