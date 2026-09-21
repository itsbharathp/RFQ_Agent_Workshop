import json
import time
try:
    from laya import Router
    router = Router(preload=True)
except ImportError:
    print("Warning: laya module not found. Please run within the laya environment.")
    router = None

# Global Sourcing & Multilingual RFQs
# Demonstrating Laya's ability to handle massive data dumps (tokens) and non-English vendor communications.

tickets = [
    {
        "ticket_id": "LOC-1001", "sender": "Vendor_JP_Tech",
        "subject": "納期遅延のお知らせ (Notice of Delivery Delay)",
        "body": "お世話になっております。先日の関税変更に伴う通関手続きの遅れにより、発注番号PO-8812の精密モーターの納品が予定より10日ほど遅れる見込みです。生産計画の調整をお願いいたします。(Due to customs delays associated with the recent tariff changes, delivery of the precision motors for PO-8812 is expected to be delayed by about 10 days. Please adjust your production schedule.)"
    },
    {
        "ticket_id": "LOC-1002", "sender": "Vendor_DE_Engineering",
        "subject": "Spezifikationsklärung für RFQ-339 (Specification clarification)",
        "body": "Guten Tag, wir benötigen eine Klärung bezüglich der Toleranzen für das Aluminiumgehäuse in RFQ-339. Die aktuellen Zeichnungen sind widersprüchlich. Ohne eine überarbeitete CAD-Datei können wir kein verlässliches Angebot abgeben. (Hello, we need clarification regarding the tolerances for the aluminum housing in RFQ-339. The current drawings are contradictory. Without a revised CAD file, we cannot submit a reliable offer.)"
    },
    {
        "ticket_id": "LOC-1003", "sender": "Logistics_MX_Hub",
        "subject": "Retraso en el puerto por huelga (Port delay due to strike)",
        "body": "Le informamos que hay una huelga en el puerto principal que está afectando todos los envíos de exportación. Nuestros contenedores con la materia prima están retenidos. Esperamos una resolución en 48 horas, pero habrá costos de estadía adicionales. (We inform you that there is a strike at the main port affecting all export shipments. Our containers with raw materials are held up. We expect a resolution in 48 hours, but there will be additional demurrage costs.)"
    },
    {
        "ticket_id": "LOC-1004", "sender": "Automated_ERP_System",
        "subject": "Bulk RFQ Bid Data Payload [JSON_DUMP]",
        "body": '{"rfq_id":"RFQ-9999","bids":[' + '{"vendor":"V001","price":1200,"lt":21},' * 150 + '{"vendor":"V001","price":1200,"lt":21}]} ERROR: Parsing limit exceeded on massive bid payload. Buffer overflow in legacy ingestion queue.'
    },
    {
        "ticket_id": "LOC-1005", "sender": "Vendor_FR_Casting",
        "subject": "Augmentation des coûts des matières premières",
        "body": "En raison des récentes augmentations des tarifs de l'acier, nous sommes contraints de réviser nos prix à la hausse de 8% pour toutes les nouvelles commandes à partir de la semaine prochaine. Merci de votre compréhension. (Due to recent steel tariff increases, we are forced to revise our prices upward by 8% for all new orders starting next week. Thank you for your understanding.)"
    }
]

questions = {
    "queue": {
        "type": "choice",
        "instructions": "Which Meridian team handles this?",
        "criteria": {
            "logistics": "delivery delays, port strikes, customs, tracking",
            "engineering": "blueprint tolerances, CAD files, technical specifications",
            "strategic_sourcing": "price increases, raw material costs, bid data processing"
        }
    },
    "urgency": {
        "type": "score",
        "instructions": "How urgent is this issue to the global supply chain?",
        "criteria": ["low priority", "medium priority", "high priority", "critical stoppage"]
    }
}

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 DEMO: SCENARIO 4 - GLOBAL SOURCING & MULTILINGUAL (MERIDIAN)")
    print("="*70 + "\n")
    
    for t in tickets:
        print(f"🎫 TICKET: {t['ticket_id']} | SENDER: {t['sender']}")
        print(f"📌 SUBJECT: {t['subject']}")
        
        if router:
            res = router.predict(t, questions)
            print(f"   [Routing] Model: {res.get('routing', {}).get('model', 'N/A')}")
            print(f"   [Queue]   Assigned: {res['answers']['queue']['choice']}")
            print(f"   [Urgency] Score: {res['answers']['urgency']['score']:.2f}")
        else:
            print("   [Dry Run] Model evaluation skipped (laya not loaded).")
        print("-" * 70)
        time.sleep(0.5)
