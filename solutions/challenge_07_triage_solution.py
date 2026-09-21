import json
import time
from laya import Router

def load_inbox():
    with open("vendor_inbox.json", "r", encoding="utf-8") as f:
        return json.load(f)

def setup_laya_questions():
    """Define the System 1 decision primitives."""
    questions = {
        "queue": {
            "type": "choice",
            "instructions": "Which department queue should this email be routed to?",
            "criteria": {
                "engineering": "technical specifications, blueprints, tolerances, CAD, thermal expansion",
                "logistics": "shipping, delivery dates, container tracking, customs, delays",
                "finance": "invoices, credit holds, past due balances, payments",
                "procurement": "vendor consolidation, contract negotiations, tariffs, strategic reviews",
                "spam": "marketing, SEO, unsolicited promotions, discounts"
            }
        },
        "urgency": {
            "type": "score",
            "instructions": "How urgent or critical is this communication?",
            "criteria": [
                "routine spam or automated notification",
                "general inquiry or minor clarification",
                "moderate delay or warning",
                "significant disruption or price increase",
                "severe threat to partnership, credit hold, or massive supply chain shock"
            ]
        }
    }
    return questions

def run_triage(inbox, questions):
    """Process the inbox through the Laya Routing Engine."""
    print("Initializing System 1 Front Door...")
    
    # Initialize the Router, preloading to avoid cold-swap delays between English and Multilingual models
    router = Router(preload=True)
    
    results = []
    
    print("\n--- Processing Inbox ---")
    start_time = time.time()
    
    for email in inbox:
        state = {
            "sender": email["sender"],
            "subject": email["subject"],
            "body": email["body"]
        }
        
        # Single forward pass evaluates all questions
        res = router.predict(state, questions)
        
        email["queue_assignment"] = res["answers"]["queue"]["choice"]
        email["urgency_score"] = round(res["answers"]["urgency"]["score"], 2)
        email["routed_language_model"] = res["routing"]["model"]
        
        print(f"[{email['id']}] Routed to: {email['queue_assignment'].upper()} | Urgency: {email['urgency_score']} | Model: {email['routed_language_model']}")
        
        results.append(email)
        
    end_time = time.time()
    
    print(f"\nProcessed {len(inbox)} emails in {(end_time - start_time):.2f} seconds.")
    print(f"Average time per email: {((end_time - start_time) / len(inbox)) * 1000:.1f} ms")
    
    return results

def extract_critical_alerts(results):
    """Filter for emails with high urgency."""
    critical_alerts = [email for email in results if email["urgency_score"] >= 3.5]
    
    print(f"\nFiltered {len(critical_alerts)} critical alerts requiring System 2 (Watchdog) review.")
    return critical_alerts

def main():
    inbox = load_inbox()
    print(f"Loaded {len(inbox)} raw emails from the inbox.")
    
    questions = setup_laya_questions()
    
    results = run_triage(inbox, questions)
    critical_alerts = extract_critical_alerts(results)
    
    with open("critical_alerts.json", "w", encoding="utf-8") as f:
        json.dump(critical_alerts, f, indent=2, ensure_ascii=False)
    
    print("\nChallenge 7 completed! Results saved to critical_alerts.json")

if __name__ == "__main__":
    main()