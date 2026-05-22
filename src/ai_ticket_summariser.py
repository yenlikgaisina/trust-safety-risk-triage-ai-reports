"""
AI-Assisted Ticket Summariser
Project: AI Trust & Safety Operations Case Study

This script creates structured reviewer summaries for synthetic Trust & Safety tickets.

It does not use a live AI API. Instead, it demonstrates the logic of an AI-assisted
summarisation workflow using deterministic, reproducible templates.

Inputs:
- data/synthetic_user_reports.csv

Outputs:
- data/synthetic_user_reports_with_summaries.csv
- reports/ticket_summariser_examples.md

Purpose:
- summarise messy user reports
- explain risk rationale
- suggest reviewer next steps
- support human-in-the-loop triage
- demonstrate responsible AI workflow design
"""

from pathlib import Path

import pandas as pd


# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "synthetic_user_reports.csv"
OUTPUT_DATA_PATH = PROJECT_ROOT / "data" / "synthetic_user_reports_with_summaries.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"
EXAMPLES_REPORT_PATH = REPORTS_DIR / "ticket_summariser_examples.md"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. Load data
# ------------------------------------------------------------

def load_data(path: Path) -> pd.DataFrame:
    """Load the synthetic ticket dataset."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at: {path}")

    df = pd.read_csv(path)

    required_columns = [
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

    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df["model_confidence"] = pd.to_numeric(df["model_confidence"], errors="coerce")
    df["human_review_required"] = df["human_review_required"].astype(str).str.lower().map(
        {"true": True, "false": False}
    )

    return df


df = load_data(DATA_PATH)


# ------------------------------------------------------------
# 3. Summary logic
# ------------------------------------------------------------

CATEGORY_RATIONALES = {
    "Account abuse": "The report suggests possible unauthorised access, suspicious login activity, or account misuse.",
    "Scam or fraud": "The report suggests possible deception, impersonation, suspicious payment behaviour, or financial harm.",
    "Harassment": "The report suggests targeted abuse, repeated unwanted contact, intimidation, or threatening behaviour.",
    "Self-harm concern": "The report includes a potential safety concern involving emotional distress, crisis language, or concern for another user.",
    "Misinformation": "The report suggests potentially false or misleading information that may create harm if left unreviewed.",
    "Privacy concern": "The report suggests possible exposure, misuse, or unauthorised sharing of personal information.",
    "Billing safety escalation": "The report links a billing issue with possible fraud, coercion, account misuse, or suspicious activity.",
    "Policy confusion": "The report appears to involve user confusion about a moderation decision, policy rule, appeal, or feature restriction.",
    "Child safety concern": "The report may involve a minor or possible risk to someone under 18, requiring specialist review.",
    "Platform integrity": "The report suggests spam, fake accounts, bot-like behaviour, coordinated manipulation, or platform abuse.",
}

SEVERITY_RATIONALES = {
    "Low": "Low severity indicates no immediate harm signal and can usually be handled through standard support or user education.",
    "Medium": "Medium severity indicates plausible risk or unclear evidence requiring timely review.",
    "High": "High severity indicates a clear risk signal requiring specialist review and faster action.",
    "Critical": "Critical severity indicates immediate or severe safety risk requiring urgent escalation.",
}

REVIEW_GUIDANCE = {
    "Trust & Safety Review": "Reviewer should assess safety context, evidence of abuse, potential harm, and whether further escalation is needed.",
    "Child Safety Escalation": "Specialist reviewer should assess possible minor involvement and follow child safety escalation procedures.",
    "Fraud and Account Integrity": "Reviewer should assess account compromise, scam signals, impersonation, suspicious payments, or coordinated abuse.",
    "Privacy Review": "Reviewer should assess whether personal data was exposed, shared without consent, or requires removal/escalation.",
    "Policy Review": "Reviewer should assess whether the issue requires policy interpretation, appeal handling, or content review.",
    "Support / Education": "Support reviewer should provide clear guidance, policy explanation, or next steps for the user.",
    "Human Review Queue": "A human reviewer should manually assess the ticket because the automated signal may be uncertain or ambiguous.",
}


def create_ticket_summary(row: pd.Series) -> str:
    """Create a concise reviewer-facing ticket summary."""
    return (
        f"User reports: {row['user_report']} "
        f"Primary risk category is {row['risk_category']} with subcategory {row['subcategory']}."
    )


def create_risk_rationale(row: pd.Series) -> str:
    """Explain why the ticket was classified this way."""
    category_rationale = CATEGORY_RATIONALES.get(
        row["risk_category"],
        "The report contains a risk signal requiring review.",
    )

    severity_rationale = SEVERITY_RATIONALES.get(
        row["severity"],
        "The severity level should be reviewed using the taxonomy and escalation decision tree.",
    )

    return f"{category_rationale} {severity_rationale}"


def create_reviewer_next_step(row: pd.Series) -> str:
    """Suggest the next operational action for a reviewer."""
    team_guidance = REVIEW_GUIDANCE.get(
        row["escalation_team"],
        "Reviewer should assess the report and determine the correct next step.",
    )

    if row["severity"] == "Critical":
        urgency = "Prioritise immediately because this is a Critical severity ticket."
    elif row["severity"] == "High":
        urgency = "Prioritise for same-day specialist review because this is a High severity ticket."
    elif row["model_confidence"] < 0.75:
        urgency = "Review manually because model confidence is below the human review threshold."
    elif row["human_review_required"]:
        urgency = "Manual review is required based on risk rules."
    else:
        urgency = "This can follow the standard review path unless new risk evidence appears."

    return f"{urgency} {team_guidance}"


def create_sla_note(row: pd.Series) -> str:
    """Create a short SLA note."""
    return (
        f"Target response time is {row['sla_target_hours']} hours "
        f"based on {row['severity']} severity."
    )


def create_human_review_note(row: pd.Series) -> str:
    """Explain whether human review is required."""
    if row["human_review_required"]:
        if row["severity"] in ["High", "Critical"]:
            return "Human review is required because the ticket is High or Critical severity."
        if row["model_confidence"] < 0.75:
            return "Human review is required because model confidence is below 0.75."
        return "Human review is required because the ticket matches a sensitive or higher-risk category."

    return "Human review is not automatically required, but the ticket can be escalated if new risk evidence appears."


def create_structured_summary(row: pd.Series) -> str:
    """Create a complete structured summary for reviewer workflow."""
    return (
        f"Summary: {create_ticket_summary(row)}\n"
        f"Risk rationale: {create_risk_rationale(row)}\n"
        f"Recommended next step: {create_reviewer_next_step(row)}\n"
        f"SLA note: {create_sla_note(row)}\n"
        f"Human review note: {create_human_review_note(row)}"
    )


# ------------------------------------------------------------
# 4. Apply summarisation
# ------------------------------------------------------------

df["ticket_summary"] = df.apply(create_ticket_summary, axis=1)
df["risk_rationale"] = df.apply(create_risk_rationale, axis=1)
df["reviewer_next_step"] = df.apply(create_reviewer_next_step, axis=1)
df["sla_note"] = df.apply(create_sla_note, axis=1)
df["human_review_note"] = df.apply(create_human_review_note, axis=1)
df["structured_reviewer_summary"] = df.apply(create_structured_summary, axis=1)


# ------------------------------------------------------------
# 5. Save enriched dataset
# ------------------------------------------------------------

df.to_csv(OUTPUT_DATA_PATH, index=False)


# ------------------------------------------------------------
# 6. Create markdown examples report
# ------------------------------------------------------------

def select_examples(data: pd.DataFrame) -> pd.DataFrame:
    """Select useful examples across severity levels and risk categories."""
    examples = []

    for severity in ["Critical", "High", "Medium", "Low"]:
        subset = data[data["severity"] == severity]
        if not subset.empty:
            examples.append(subset.iloc[0])

    sensitive_categories = [
        "Child safety concern",
        "Self-harm concern",
        "Privacy concern",
        "Scam or fraud",
        "Account abuse",
        "Policy confusion",
    ]

    for category in sensitive_categories:
        subset = data[data["risk_category"] == category]
        if not subset.empty:
            examples.append(subset.iloc[0])

    examples_df = pd.DataFrame(examples).drop_duplicates(subset=["ticket_id"])
    return examples_df.head(10)


examples_df = select_examples(df)


def create_example_block(row: pd.Series) -> str:
    """Create markdown block for one example ticket."""
    return f"""## Example: {row["ticket_id"]}

| Field | Value |
|---|---|
| Created at | {row["created_at"]} |
| Risk category | {row["risk_category"]} |
| Subcategory | {row["subcategory"]} |
| Severity | {row["severity"]} |
| SLA target | {row["sla_target_hours"]} hours |
| Escalation team | {row["escalation_team"]} |
| Model confidence | {row["model_confidence"]} |
| Human review required | {row["human_review_required"]} |
| Final action | {row["final_action"]} |

### Original User Report

> {row["user_report"]}

### AI-Assisted Reviewer Summary

{row["structured_reviewer_summary"]}
"""


example_blocks = "\n".join(
    create_example_block(row) for _, row in examples_df.iterrows()
)

human_review_count = int(df["human_review_required"].sum())
low_confidence_count = int((df["model_confidence"] < 0.75).sum())
critical_count = int((df["severity"] == "Critical").sum())
high_count = int((df["severity"] == "High").sum())

examples_report = f"""# AI-Assisted Ticket Summariser Examples

## Project Context

This report is part of the portfolio project:

**AI Trust & Safety Operations Case Study: Risk Triage, Taxonomy Design and Escalation Workflow**

The summariser creates structured reviewer notes for synthetic Trust & Safety user reports.

No real users, platforms, accounts, companies, or incidents are included.

## Purpose

The purpose of this script is to demonstrate how AI-assisted summarisation could support Trust & Safety reviewers by turning free-text user reports into structured review notes.

The generated summaries are designed to help reviewers quickly understand:

- what the user reported
- why the ticket was classified into a risk category
- why the severity level matters
- which team should review the case
- whether human review is required
- what the next operational step should be

## Important Responsible AI Note

This script does not use a live AI model or external API.

It uses deterministic templates so the workflow is reproducible, transparent, and safe for a public portfolio project.

In a production environment, AI-generated summaries should be treated as reviewer support only. They should not replace human judgement in High, Critical, child safety, self-harm, fraud, privacy, or ambiguous cases.

## Summary Metrics

| Metric | Value |
|---|---:|
| Total tickets summarised | {len(df)} |
| Critical tickets | {critical_count} |
| High tickets | {high_count} |
| Tickets requiring human review | {human_review_count} |
| Low-confidence tickets | {low_confidence_count} |

## Output Dataset

The enriched dataset with reviewer summaries has been saved to:

```text
data/synthetic_user_reports_with_summaries.csv
```

## Example Summaries

{example_blocks}

## Portfolio Relevance

This script demonstrates skills in:

- AI-assisted workflow design
- Trust & Safety triage operations
- reviewer support tooling
- human-in-the-loop process design
- responsible AI documentation
- structured summarisation
- escalation support
- reproducible data processing
- portfolio-ready automation

## Limitations

This summariser is a deterministic portfolio demonstration. It does not understand user reports like a real language model would.

Limitations include:

- summaries are template-based
- no real natural language generation model is used
- no real policy decision-making is performed
- no real users or incidents are included
- outputs should be reviewed by humans before any operational use
- production use would require testing, monitoring, privacy review, and policy validation
"""

EXAMPLES_REPORT_PATH.write_text(examples_report, encoding="utf-8")


# ------------------------------------------------------------
# 7. Print results
# ------------------------------------------------------------

print("AI-assisted ticket summarisation complete.")
print(f"Tickets summarised: {len(df)}")
print(f"Enriched dataset saved to: {OUTPUT_DATA_PATH}")
print(f"Examples report saved to: {EXAMPLES_REPORT_PATH}")
print(f"Human review required tickets: {human_review_count}")
print(f"Low-confidence tickets: {low_confidence_count}")
