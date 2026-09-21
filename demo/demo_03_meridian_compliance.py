import json
import time
try:
    from laya import Router
    router = Router(preload=True)
except ImportError:
    print("Warning: laya module not found. Please run within the laya environment.")
    router = None

# Tariff Shocks & Trade Compliance
# Evaluating market signals, tariff impacts, and trade compliance (ITAR/Export) risks.

tickets = [
    {
        "ticket_id": "CMP-9901", "sender": "Global_Trade_Watch",
        "subject": "MARKET ALERT: 15% Tariff on Imported Electronics",
        "body": "Effective September 1st, a new 15% tariff is being applied to all imported industrial control electronics and PLCs. This will directly impact COGS for any Work Orders relying on overseas PCB assembly. Procurement needs to adjust cost models immediately."
    },
    {
        "ticket_id": "CMP-9902", "sender": "Internal_Audit",
        "subject": "ITAR Violation Risk in RFQ-5521",
        "body": "Urgent: We attached the full unredacted blueprint for the defense contractor actuator to RFQ-5521, which was sent to three non-US-based suppliers. This is a potential ITAR export control violation. We must recall the RFQ and notify the legal department to assess exposure."
    },
    {
        "ticket_id": "CMP-9903", "sender": "Vendor_V009",
        "subject": "Rare Earth Metal Surcharges",
        "body": "Due to recent export quotas from primary mining nations, the spot price for neodymium has spiked 40%. We are invoking the force majeure clause in our contract to apply an emergency raw material surcharge to all pending POs."
    },
    {
        "ticket_id": "CMP-9904", "sender": "Security_Ops",
        "subject": "Confidential Pricing Matrix Exposed in Public S3",
        "body": "A purchasing agent accidentally uploaded the 2024 negotiated vendor pricing matrix to a publicly accessible cloud bucket instead of the secure intranet portal. The file `meridian_vendor_margins_24.csv` was downloaded 12 times before being secured. Initiating incident response."
    },
    {
        "ticket_id": "CMP-9905", "sender": "Commodity_Manager",
        "subject": "Competitor Capacity Buyout",
        "body": "Market Intel: Our primary competitor just secured a 2-year exclusive capacity agreement with our secondary casting supplier. We need to lock in long-term contracts with our remaining foundries before they leverage this shortage against us."
    }
]

questions = {
    "queue": {
        "type": "choice",
        "instructions": "Which team handles this compliance or market event?",
        "criteria": {
            "legal_trade": "ITAR violations, export controls, force majeure clauses",
            "security": "data leaks, exposed pricing, unauthorized access",
            "procurement_ops": "tariffs, commodity pricing shocks, competitor buyouts"
        }
    },
    "urgency": {
        "type": "score",
        "instructions": "How critical is this compliance or market risk?",
        "criteria": ["routine update", "needs review", "immediate business impact", "critical legal/security incident"]
    },
    "compliance_breach": {
        "type": "noul",
        "instructions": "Does this message describe a direct violation of compliance, data security, or export laws?"
    }
}

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 DEMO: SCENARIO 3 - TARIFF SHOCKS & TRADE COMPLIANCE (MERIDIAN)")
    print("="*70 + "\n")
    
    for t in tickets:
        print(f"🎫 TICKET: {t['ticket_id']} | SENDER: {t['sender']}")
        print(f"📌 SUBJECT: {t['subject']}")
        
        if router:
            res = router.predict(t, questions)
            print(f"   [Routing] Model: {res.get('routing', {}).get('model', 'N/A')}")
            print(f"   [Queue]   Assigned: {res['answers']['queue']['choice']}")
            print(f"   [Urgency] Score: {res['answers']['urgency']['score']:.2f}")
            breach = res['answers']['compliance_breach'].get('noul', 0)
            print(f"   [Breach]  Risk: {breach:.1%}")
            
            if breach > 0.6:
                print("   🚨 ALERT: POTENTIAL COMPLIANCE BREACH. REDACTING CONTENT & ROUTING TO LEGAL. 🚨")
        else:
            print("   [Dry Run] Model evaluation skipped (laya not loaded).")
        print("-" * 70)
        time.sleep(0.5)
