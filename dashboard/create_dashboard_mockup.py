"""
Dashboard Mockup Generator
Project: AI Trust & Safety Operations Case Study

This script creates a static dashboard mockup image using the synthetic Trust & Safety triage dataset.

Input:
- data/synthetic_user_reports.csv

Outputs:
- images/dashboard_mockup.png
- images/dashboard_priority_queue.png
- dashboard/dashboard_summary_metrics.md

Purpose:
- create portfolio-ready dashboard screenshots
- visualise risk category, severity, human review, escalation workload,
  and model confidence
- demonstrate how Trust & Safety operations can be monitored with
  responsible AI safeguards
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "synthetic_user_reports.csv"
IMAGES_DIR = PROJECT_ROOT / "images"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"

DASHBOARD_MOCKUP_PATH = IMAGES_DIR / "dashboard_mockup.png"
PRIORITY_QUEUE_PATH = IMAGES_DIR / "dashboard_priority_queue.png"
SUMMARY_METRICS_PATH = DASHBOARD_DIR / "dashboard_summary_metrics.md"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. Load data
# ------------------------------------------------------------

def load_data(path: Path) -> pd.DataFrame:
    """Load and prepare the synthetic ticket dataset."""
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

    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["model_confidence"] = pd.to_numeric(df["model_confidence"], errors="coerce")
    df["sla_target_hours"] = pd.to_numeric(df["sla_target_hours"], errors="coerce")

    df["human_review_required"] = (
        df["human_review_required"]
        .astype(str)
        .str.lower()
        .map({"true": True, "false": False})
    )

    return df


df = load_data(DATA_PATH)


# ------------------------------------------------------------
# 3. Dashboard metrics
# ------------------------------------------------------------

total_tickets = len(df)
critical_tickets = int((df["severity"] == "Critical").sum())
high_tickets = int((df["severity"] == "High").sum())
urgent_tickets = int(df["severity"].isin(["High", "Critical"]).sum())
human_review_tickets = int(df["human_review_required"].sum())
low_confidence_tickets = int((df["model_confidence"] < 0.75).sum())
average_model_confidence = round(float(df["model_confidence"].mean()), 3)

urgent_percentage = round(urgent_tickets / total_tickets * 100, 1)
human_review_percentage = round(human_review_tickets / total_tickets * 100, 1)
low_confidence_percentage = round(low_confidence_tickets / total_tickets * 100, 1)

risk_category_counts = (
    df["risk_category"]
    .value_counts()
    .sort_values(ascending=True)
)

severity_order = ["Low", "Medium", "High", "Critical"]
severity_counts = (
    df["severity"]
    .value_counts()
    .reindex(severity_order)
    .fillna(0)
)

escalation_team_counts = (
    df["escalation_team"]
    .value_counts()
    .sort_values(ascending=True)
)

human_review_counts = (
    df["human_review_required"]
    .value_counts()
    .rename(index={True: "Human review required", False: "No automatic review"})
)

confidence_by_category = (
    df.groupby("risk_category")["model_confidence"]
    .mean()
    .sort_values(ascending=True)
)

final_action_counts = (
    df["final_action"]
    .value_counts()
    .sort_values(ascending=True)
)


# ------------------------------------------------------------
# 4. Helper functions
# ------------------------------------------------------------

def add_kpi_card(ax, title: str, value: str, subtitle: str) -> None:
    """Create a simple KPI card."""
    ax.axis("off")
    ax.text(
        0.5,
        0.68,
        value,
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold",
    )
    ax.text(
        0.5,
        0.40,
        title,
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
    )
    ax.text(
        0.5,
        0.20,
        subtitle,
        ha="center",
        va="center",
        fontsize=9,
    )
    ax.add_patch(
        plt.Rectangle(
            (0.02, 0.02),
            0.96,
            0.96,
            fill=False,
            linewidth=1,
            transform=ax.transAxes,
            clip_on=False,
        )
    )


def style_axis(ax, title: str) -> None:
    """Apply simple styling to chart axes."""
    ax.set_title(title, fontsize=12, fontweight="bold", pad=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=0.3)


# ------------------------------------------------------------
# 5. Create main dashboard mockup
# ------------------------------------------------------------

fig = plt.figure(figsize=(18, 14))
fig.suptitle(
    "AI Trust & Safety Risk Triage Dashboard",
    fontsize=24,
    fontweight="bold",
    y=0.98,
)

fig.text(
    0.5,
    0.952,
    "Synthetic user report analysis for risk classification, escalation, human review, and responsible AI monitoring",
    ha="center",
    fontsize=11,
)

grid = fig.add_gridspec(
    nrows=4,
    ncols=4,
    height_ratios=[1.0, 2.2, 2.2, 2.2],
    hspace=0.55,
    wspace=0.35,
)

# KPI cards
add_kpi_card(
    fig.add_subplot(grid[0, 0]),
    "Total Tickets",
    f"{total_tickets:,}",
    "Synthetic reports analysed",
)

add_kpi_card(
    fig.add_subplot(grid[0, 1]),
    "High + Critical",
    f"{urgent_tickets:,}",
    f"{urgent_percentage}% of all tickets",
)

add_kpi_card(
    fig.add_subplot(grid[0, 2]),
    "Human Review Required",
    f"{human_review_tickets:,}",
    f"{human_review_percentage}% of all tickets",
)

add_kpi_card(
    fig.add_subplot(grid[0, 3]),
    "Low Confidence",
    f"{low_confidence_tickets:,}",
    f"{low_confidence_percentage}% below 0.75",
)

# Chart 1: Risk category counts
ax1 = fig.add_subplot(grid[1, 0:2])
risk_category_counts.plot(kind="barh", ax=ax1)
style_axis(ax1, "Tickets by Risk Category")
ax1.set_xlabel("Ticket Count")
ax1.set_ylabel("Risk Category")

# Chart 2: Severity counts
ax2 = fig.add_subplot(grid[1, 2])
severity_counts.plot(kind="bar", ax=ax2)
style_axis(ax2, "Tickets by Severity")
ax2.set_xlabel("Severity")
ax2.set_ylabel("Ticket Count")
ax2.tick_params(axis="x", rotation=45)

# Chart 3: Human review split
ax3 = fig.add_subplot(grid[1, 3])
human_review_counts.plot(kind="bar", ax=ax3)
style_axis(ax3, "Human Review Requirement")
ax3.set_xlabel("")
ax3.set_ylabel("Ticket Count")
ax3.tick_params(axis="x", rotation=25)

# Chart 4: Escalation team workload
ax4 = fig.add_subplot(grid[2, 0:2])
escalation_team_counts.plot(kind="barh", ax=ax4)
style_axis(ax4, "Escalation Team Workload")
ax4.set_xlabel("Ticket Count")
ax4.set_ylabel("Escalation Team")

# Chart 5: Model confidence by category
ax5 = fig.add_subplot(grid[2, 2:4])
confidence_by_category.plot(kind="barh", ax=ax5)
style_axis(ax5, "Average Model Confidence by Risk Category")
ax5.set_xlabel("Average Model Confidence")
ax5.set_ylabel("Risk Category")
ax5.set_xlim(0, 1)

# Chart 6: Final action distribution
ax6 = fig.add_subplot(grid[3, 0:2])
final_action_counts.plot(kind="barh", ax=ax6)
style_axis(ax6, "Final Action Distribution")
ax6.set_xlabel("Ticket Count")
ax6.set_ylabel("Final Action")

# Chart 7: Responsible AI safeguard summary
ax7 = fig.add_subplot(grid[3, 2:4])
ax7.axis("off")

safeguard_text = f"""
Responsible AI Safeguard Checks

• High and Critical tickets require human review.
• Low-confidence tickets below 0.75 are routed to human review.
• Sensitive categories are escalated to specialist teams.
• Model confidence is monitored by risk category.
• Human review is treated as a safety control, not a process failure.

Current dataset summary:
• Critical tickets: {critical_tickets}
• High tickets: {high_tickets}
• Average model confidence: {average_model_confidence}
• Human review required: {human_review_tickets} tickets
• Low-confidence tickets: {low_confidence_tickets}
"""

ax7.text(
    0.03,
    0.95,
    safeguard_text,
    va="top",
    fontsize=12,
    linespacing=1.5,
)

ax7.add_patch(
    plt.Rectangle(
        (0.01, 0.01),
        0.98,
        0.98,
        fill=False,
        linewidth=1,
        transform=ax7.transAxes,
        clip_on=False,
    )
)

plt.savefig(DASHBOARD_MOCKUP_PATH, dpi=300, bbox_inches="tight")
plt.close()


# ------------------------------------------------------------
# 6. Create priority queue image
# ------------------------------------------------------------

priority_queue = df.copy()

priority_queue["priority_rank"] = priority_queue.apply(
    lambda row: 1
    if row["severity"] == "Critical"
    else 2
    if row["severity"] == "High"
    else 3
    if row["model_confidence"] < 0.75
    else 4
    if row["severity"] == "Medium"
    else 5,
    axis=1,
)

priority_queue = priority_queue.sort_values(
    by=["priority_rank", "model_confidence", "created_at"],
    ascending=[True, True, True],
)

priority_table = priority_queue[
    [
        "ticket_id",
        "risk_category",
        "severity",
        "sla_target_hours",
        "model_confidence",
        "escalation_team",
        "human_review_required",
    ]
].head(12)

fig, ax = plt.subplots(figsize=(16, 7))
ax.axis("off")
ax.set_title(
    "Priority Review Queue Sample",
    fontsize=18,
    fontweight="bold",
    pad=20,
)

table = ax.table(
    cellText=priority_table.values,
    colLabels=[
        "Ticket ID",
        "Risk Category",
        "Severity",
        "SLA Hours",
        "Confidence",
        "Escalation Team",
        "Human Review",
    ],
    loc="center",
    cellLoc="left",
)

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.8)

for key, cell in table.get_celld().items():
    cell.set_linewidth(0.5)
    if key[0] == 0:
        cell.set_text_props(weight="bold")

plt.savefig(PRIORITY_QUEUE_PATH, dpi=300, bbox_inches="tight")
plt.close()


# ------------------------------------------------------------
# 7. Create dashboard summary metrics markdown
# ------------------------------------------------------------

summary_markdown = f"""# Dashboard Summary Metrics

## Project Context

This dashboard summary is part of the portfolio project:

**AI Trust & Safety Operations Case Study: Risk Triage, Taxonomy Design and Escalation Workflow**

The dashboard uses fully synthetic user report data. No real users, accounts, platforms, companies, or incidents are included.

## Dashboard Outputs

| Output | Location |
|---|---|
| Main dashboard mockup | images/dashboard_mockup.png |
| Priority queue table image | images/dashboard_priority_queue.png |

## Executive Metrics

| Metric | Value |
|---|---:|
| Total tickets | {total_tickets} |
| Critical tickets | {critical_tickets} |
| High tickets | {high_tickets} |
| High + Critical tickets | {urgent_tickets} |
| High + Critical percentage | {urgent_percentage}% |
| Human review required tickets | {human_review_tickets} |
| Human review required percentage | {human_review_percentage}% |
| Low-confidence tickets | {low_confidence_tickets} |
| Low-confidence percentage | {low_confidence_percentage}% |
| Average model confidence | {average_model_confidence} |

## Risk Category Counts

{risk_category_counts.sort_values(ascending=False).rename_axis("risk_category").reset_index(name="ticket_count").to_markdown(index=False)}

## Severity Counts

{severity_counts.rename_axis("severity").reset_index(name="ticket_count").to_markdown(index=False)}

## Escalation Team Workload

{escalation_team_counts.sort_values(ascending=False).rename_axis("escalation_team").reset_index(name="ticket_count").to_markdown(index=False)}

## Average Model Confidence by Risk Category

{confidence_by_category.rename_axis("risk_category").reset_index(name="average_model_confidence").to_markdown(index=False)}

## Dashboard Interpretation

The dashboard shows how synthetic Trust & Safety user reports can be monitored across risk category, severity, escalation workload, human review requirement, and model confidence.

The key operational focus areas are:

1. High and Critical tickets that require urgent review.
2. Categories with high human review demand.
3. Escalation teams receiving the largest workload.
4. Low-confidence model predictions that should not be handled by automation alone.
5. Sensitive categories where human oversight is required.

## Responsible AI Notes

The dashboard makes AI uncertainty visible by showing model confidence and low-confidence ticket volume.

Human review is treated as a responsible AI safeguard. High-risk, sensitive, ambiguous, and low-confidence cases should be reviewed by humans rather than handled through automation alone.
"""

SUMMARY_METRICS_PATH.write_text(summary_markdown, encoding="utf-8")


# ------------------------------------------------------------
# 8. Print results
# ------------------------------------------------------------

print("Dashboard mockup generation complete.")
print(f"Main dashboard saved to: {DASHBOARD_MOCKUP_PATH}")
print(f"Priority queue image saved to: {PRIORITY_QUEUE_PATH}")
print(f"Summary metrics saved to: {SUMMARY_METRICS_PATH}")
print("")
print("Executive metrics:")
print(f"- Total tickets: {total_tickets}")
print(f"- Critical tickets: {critical_tickets}")
print(f"- High tickets: {high_tickets}")
print(f"- High + Critical tickets: {urgent_tickets} ({urgent_percentage}%)")
print(f"- Human review required: {human_review_tickets} ({human_review_percentage}%)")
print(f"- Low-confidence tickets: {low_confidence_tickets} ({low_confidence_percentage}%)")
print(f"- Average model confidence: {average_model_confidence}")
