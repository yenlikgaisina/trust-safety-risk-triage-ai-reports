import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUTPUT_PATH = Path("data/synthetic_user_reports.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

RISK_CONFIG = {
    "Account abuse": {
        "subcategories": [
            "unauthorised_login",
            "suspicious_login_attempt",
            "credential_stuffing_suspected",
            "session_hijack_suspected",
            "account_settings_changed",
            "account_recovery_abuse",
        ],
        "severity_options": ["Medium", "High"],
        "team": "Fraud and Account Integrity",
        "actions": ["Account security review", "Human review required"],
        "templates": [
            "Someone changed my password and I cannot access my account.",
            "I received a login alert from a location I do not recognise.",
            "My account settings were changed without my permission.",
            "I think someone is trying to break into my account repeatedly.",
            "My recovery email was changed and I did not request it.",
        ],
    },
    "Scam or fraud": {
        "subcategories": [
            "impersonation",
            "off_platform_payment",
            "fake_offer",
            "advance_fee_scam",
            "investment_scam",
            "phishing_attempt",
            "refund_abuse",
        ],
        "severity_options": ["High"],
        "team": "Fraud and Account Integrity",
        "actions": ["Fraud investigation", "Human review required"],
        "templates": [
            "This account is pretending to be someone else and asking people for money.",
            "A user asked me to send payment through a private link.",
            "I received a suspicious message promising a fake investment return.",
            "Someone sent me a link that looks like a phishing attempt.",
            "A user offered a service but asked me to pay outside the platform.",
        ],
    },
    "Harassment": {
        "subcategories": [
            "targeted_insults",
            "repeated_unwanted_contact",
            "threats",
            "hate_directed_abuse",
            "sexual_harassment",
            "intimidation",
        ],
        "severity_options": ["Medium", "High"],
        "team": "Trust & Safety Review",
        "actions": ["Content review", "Safety escalation", "Human review required"],
        "templates": [
            "A user keeps sending me unwanted messages after I asked them to stop.",
            "Someone is repeatedly insulting me in comments.",
            "I received threatening messages from another account.",
            "A group of users are targeting me with abusive replies.",
            "Someone is making intimidating comments toward me.",
        ],
    },
    "Self-harm concern": {
        "subcategories": [
            "self_disclosure",
            "crisis_language",
            "concern_about_other_user",
            "potential_immediate_risk",
            "non_immediate_distress",
        ],
        "severity_options": ["High", "Critical"],
        "team": "Trust & Safety Review",
        "actions": ["Safety escalation", "Human review required"],
        "templates": [
            "I am worried that another user may hurt themselves based on their recent messages.",
            "A user posted something that sounds like they are in crisis.",
            "Someone said they do not feel safe and may harm themselves.",
            "I saw a message from a user saying they cannot continue anymore.",
            "A user appears to be asking for help during a serious emotional crisis.",
        ],
    },
    "Misinformation": {
        "subcategories": [
            "health_misinformation",
            "safety_misinformation",
            "manipulated_media",
            "misleading_claims",
            "harmful_instructional_content",
        ],
        "severity_options": ["Medium", "High"],
        "team": "Policy Review",
        "actions": ["Policy review", "Content review", "Human review required"],
        "templates": [
            "This post is sharing dangerous health advice that could harm people.",
            "A user is spreading misleading safety information.",
            "This video appears to be manipulated and presented as real.",
            "A post is making false claims that could lead people to unsafe behaviour.",
            "Someone is sharing instructions that may cause harm if followed.",
        ],
    },
    "Privacy concern": {
        "subcategories": [
            "personal_data_exposure",
            "unauthorised_sharing",
            "deletion_request",
            "doxxing_concern",
            "visibility_misconfiguration",
        ],
        "severity_options": ["Medium", "High"],
        "team": "Privacy Review",
        "actions": ["Privacy escalation", "Human review required"],
        "templates": [
            "A user posted my phone number publicly.",
            "Someone shared private information about me without permission.",
            "My personal details are visible where they should not be.",
            "I want my private information removed from this post.",
            "My address was shared in a comment without my consent.",
        ],
    },
    "Billing safety escalation": {
        "subcategories": [
            "suspicious_charge",
            "payment_method_misuse",
            "coerced_payment",
            "refund_dispute_with_fraud_signal",
            "billing_after_account_takeover",
        ],
        "severity_options": ["Medium", "High"],
        "team": "Fraud and Account Integrity",
        "actions": ["Fraud investigation", "Account security review", "Human review required"],
        "templates": [
            "I noticed a suspicious charge after my account was accessed.",
            "My payment method was used without my permission.",
            "Someone pressured me into making a payment.",
            "I requested a refund but the situation looks like fraud.",
            "I was charged after suspicious activity appeared on my account.",
        ],
    },
    "Policy confusion": {
        "subcategories": [
            "content_removal_question",
            "account_action_question",
            "feature_restriction_question",
            "appeal_request",
            "unclear_policy_application",
        ],
        "severity_options": ["Low", "Medium"],
        "team": "Support / Education",
        "actions": ["User education", "Policy review", "No action"],
        "templates": [
            "I do not understand why my post was removed.",
            "Can someone explain which rule I broke?",
            "Why was my account feature restricted?",
            "I want to appeal the decision on my content.",
            "The policy explanation was unclear to me.",
        ],
    },
    "Child safety concern": {
        "subcategories": [
            "minor_contact_concern",
            "age_appropriate_content_concern",
            "suspected_grooming_signal",
            "minor_privacy_concern",
        ],
        "severity_options": ["Critical"],
        "team": "Child Safety Escalation",
        "actions": ["Child safety escalation", "Human review required"],
        "templates": [
            "I am worried an adult is contacting my younger sibling.",
            "This content does not seem appropriate for children.",
            "A user appears to be trying to build an unsafe relationship with a minor.",
            "Private information about a child was shared publicly.",
            "I think a minor may be at risk based on this interaction.",
        ],
    },
    "Platform integrity": {
        "subcategories": [
            "spam_network",
            "coordinated_inauthentic_activity",
            "bot_like_activity",
            "fake_account_cluster",
            "scripted_abuse",
            "review_manipulation",
        ],
        "severity_options": ["Medium", "High"],
        "team": "Fraud and Account Integrity",
        "actions": ["Content review", "Fraud investigation", "Human review required"],
        "templates": [
            "Many accounts are posting the same suspicious message repeatedly.",
            "This looks like coordinated fake account activity.",
            "Several accounts appear to be bots.",
            "A group of fake accounts are manipulating reviews.",
            "The same scripted message is being posted across many accounts.",
        ],
    },
}

SLA_BY_SEVERITY = {
    "Low": 72,
    "Medium": 24,
    "High": 4,
    "Critical": 1,
}

REGIONS = [
    "UK",
    "Europe",
    "North America",
    "Asia-Pacific",
    "Middle East",
    "Africa",
    "Latin America",
    "Global / Unknown",
]

CHANNELS = [
    "Web form",
    "Mobile app",
    "Email support",
    "Live chat",
    "In-product report",
    "Appeal form",
]

LANGUAGES = [
    "English",
    "Spanish",
    "French",
    "German",
    "Arabic",
    "Russian",
    "Other",
]


def generate_created_at():
    start_date = datetime(2026, 1, 1, 8, 0, 0)
    random_days = random.randint(0, 119)
    random_minutes = random.randint(0, 1439)
    return start_date + timedelta(days=random_days, minutes=random_minutes)


def generate_confidence(severity):
    if severity in ["Critical", "High"]:
        return round(random.uniform(0.62, 0.96), 2)
    if severity == "Medium":
        return round(random.uniform(0.55, 0.94), 2)
    return round(random.uniform(0.70, 0.98), 2)


def requires_human_review(severity, confidence, category):
    sensitive_categories = {
        "Child safety concern",
        "Self-harm concern",
        "Privacy concern",
        "Scam or fraud",
        "Billing safety escalation",
    }

    return (
        severity in ["High", "Critical"]
        or confidence < 0.75
        or category in sensitive_categories
    )


def generate_ticket(ticket_number):
    category = random.choice(list(RISK_CONFIG.keys()))
    config = RISK_CONFIG[category]

    subcategory = random.choice(config["subcategories"])
    severity = random.choice(config["severity_options"])
    confidence = generate_confidence(severity)

    ticket = {
        "ticket_id": f"TKT-{ticket_number:04d}",
        "created_at": generate_created_at().strftime("%Y-%m-%d %H:%M:%S"),
        "user_report": random.choice(config["templates"]),
        "risk_category": category,
        "subcategory": subcategory,
        "severity": severity,
        "sla_target_hours": SLA_BY_SEVERITY[severity],
        "region": random.choice(REGIONS),
        "channel": random.choice(CHANNELS),
        "language": random.choice(LANGUAGES),
        "model_confidence": confidence,
        "escalation_team": config["team"],
        "human_review_required": requires_human_review(severity, confidence, category),
        "final_action": random.choice(config["actions"]),
    }

    return ticket


def main():
    fieldnames = [
        "ticket_id",
        "created_at",
        "user_report",
        "risk_category",
        "subcategory",
        "severity",
        "sla_target_hours",
        "region",
        "channel",
        "language",
        "model_confidence",
        "escalation_team",
        "human_review_required",
        "final_action",
    ]

    tickets = [generate_ticket(i) for i in range(1, 501)]

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tickets)

    print(f"Generated {len(tickets)} synthetic tickets")
    print(f"Saved dataset to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
