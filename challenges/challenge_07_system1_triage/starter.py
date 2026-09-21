import json
import time

# TODO 1: Import laya Router
# from laya import Router

def load_inbox():
    with open("vendor_inbox.json", "r", encoding="utf-8") as f:
        return json.load(f)

def setup_laya_questions():
    """Define the System 1 decision primitives."""
    # TODO 2: Configure the 'choice' primitive for queue assignment
    # Define criteria for: engineering, logistics, finance, procurement, spam
    
    # TODO 3: Configure the 'score' primitive for urgency
    # Define a 0 to 5 scale (e.g., ["routine update", "mild delay", ..., "critical threat"])
    
    questions = {
        # "queue": { ... },
        # "urgency": { ... }
    }
    return questions

def run_triage(inbox, questions):
    """Process the inbox through the Laya Routing Engine."""
    print("Initializing System 1 Front Door...")
    
    # TODO 4: Initialize the Router
    # router = Router(preload=True)
    
    results = []
    
    start_time = time.time()
    
    for email in inbox:
        state = {
            "sender": email["sender"],
            "subject": email["subject"],
            "body": email["body"]
        }
        
        # TODO 5: Call router.predict(state, questions)
        # res = router.predict(state, questions)
        
        # TODO 6: Extract the assigned queue, urgency score, and the routed language model used
        # email["queue_assignment"] = ...
        # email["urgency_score"] = ...
        # email["routed_language"] = ...
        
        results.append(email)
        
    end_time = time.time()
    
    print(f"Processed {len(inbox)} emails in {(end_time - start_time):.2f} seconds.")
    return results

def extract_critical_alerts(results):
    """Filter for emails with high urgency."""
    # TODO 7: Filter results where urgency_score >= 4.0
    critical_alerts = []
    
    print(f"Found {len(critical_alerts)} critical alerts.")
    return critical_alerts

def main():
    inbox = load_inbox()
    print(f"Loaded {len(inbox)} raw emails from the inbox.")
    
    questions = setup_laya_questions()
    
    if not questions:
        print("Please complete TODO 2 and 3 to setup Laya questions.")
        return
        
    # results = run_triage(inbox, questions)
    # critical_alerts = extract_critical_alerts(results)
    
    # with open("critical_alerts.json", "w") as f:
    #     json.dump(critical_alerts, f, indent=2)
    
    print("\nChallenge 7 completed!")

if __name__ == "__main__":
    main()