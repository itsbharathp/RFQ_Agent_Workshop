import json
import time
try:
    from laya import Router
    router = Router(preload=True)
except ImportError:
    print("Warning: laya module not found. Please run within the laya environment.")
    router = None

# Vendor Health & Supply Churn Risk
# Identifying subtle indicators of degrading vendor health, flight risk, or capacity limits.

tickets = [
    {
        "ticket_id": "VEND-001", "sender": "Vendor_V001",
        "subject": "Re: Bid Invitation RFQ-2024-09",
        "body": "Thank you for the invitation to bid. Due to our current capacity constraints and the recent 45-day payment cycles we've experienced with Meridian, we will be passing on this RFQ and prioritizing our other automotive clients. We will revisit in Q2 2025."
    },
    {
        "ticket_id": "VEND-002", "sender": "Vendor_V018",
        "subject": "Notice of Lead Time Extension",
        "body": "Effective immediately, our standard lead time for the Type-C chassis components is extending from 3 weeks to 8 weeks. We are facing severe raw material shortages and labor turnover. We cannot guarantee historical delivery SLAs for the upcoming quarter."
    },
    {
        "ticket_id": "VEND-003", "sender": "Meridian_Vendor_Relations",
        "subject": "Health Score Alert: V007 Composite Drop",
        "body": "Automated Alert: Vendor V007's composite health score has dropped from 82.4 to 61.1 over the last two months. Primary drivers: 3 consecutive late deliveries and a 40% drop in bid response rate. Intervention required."
    },
    {
        "ticket_id": "VEND-004", "sender": "Vendor_V022",
        "subject": "Invoice Discrepancy & Account Hold",
        "body": "We have three outstanding invoices over 60 days past due. As per our master service agreement, your account is now on credit hold. No new Work Orders will be processed until the balance of $112,000 is cleared."
    },
    {
        "ticket_id": "VEND-005", "sender": "Vendor_V014",
        "subject": "Excessive Admin Burden on RFQs",
        "body": "We've noticed that for the last 5 RFQs, your team has required an average of 4 rounds of technical clarification. This is driving up our overhead. We need to schedule an architecture review to align your blueprints with our standard tooling, otherwise we cannot remain competitive on pricing."
    }
]

questions = {
    "queue": {
        "type": "choice",
        "instructions": "Which Meridian team should handle this vendor communication?",
        "criteria": {
            "vendor_relations": "vendor health drops, relationship management, admin burden complaints",
            "accounts_payable": "late payments, credit holds, invoice disputes",
            "strategic_sourcing": "capacity constraints, lead time extensions, passing on bids",
        }
    },
    "urgency": {
        "type": "score",
        "instructions": "How urgent is this vendor issue regarding Meridian's supply chain continuity?",
        "criteria": ["informational only", "monitor next month", "action required this week", "critical supply stoppage"]
    },
    "supplier_flight_risk": {
        "type": "noul",
        "instructions": "Does the vendor explicitly state they are deprioritizing Meridian, passing on work, or putting the account on hold?"
    }
}

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 DEMO: SCENARIO 2 - VENDOR HEALTH & SUPPLY CHURN (MERIDIAN)")
    print("="*70 + "\n")
    
    for t in tickets:
        print(f"🎫 TICKET: {t['ticket_id']} | SENDER: {t['sender']}")
        print(f"📌 SUBJECT: {t['subject']}")
        
        if router:
            res = router.predict(t, questions)
            print(f"   [Routing] Model: {res.get('routing', {}).get('model', 'N/A')}")
            print(f"   [Queue]   Assigned: {res['answers']['queue']['choice']}")
            print(f"   [Urgency] Score: {res['answers']['urgency']['score']:.2f}")
            risk = res['answers']['supplier_flight_risk'].get('noul', 0)
            print(f"   [Flight Risk] Probability: {risk:.1%}")
            
            if risk > 0.7:
                print("   🚨 ALERT: HIGH VENDOR FLIGHT RISK DETECTED. ESCALATING TO COMMODITY MANAGER. 🚨")
        else:
            print("   [Dry Run] Model evaluation skipped (laya not loaded).")
        print("-" * 70)
        time.sleep(0.5)
