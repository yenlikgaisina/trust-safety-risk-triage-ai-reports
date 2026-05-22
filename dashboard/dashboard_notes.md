# Dashboard Notes

## Project Context

This dashboard plan is part of the portfolio project:

AI Trust & Safety Operations Case Study: Risk Triage, Taxonomy Design and Escalation Workflow

The project uses fully synthetic user reports to demonstrate how Trust & Safety teams can monitor incoming risk signals, severity levels, SLA priorities, human review demand, escalation workload, and model confidence.

No real users, platforms, accounts, companies, or incidents are used in this project.

## Dashboard Purpose

The purpose of this dashboard is to help a Trust & Safety operations team answer:

1. What types of user reports are coming in?
2. Which risks are most common?
3. How many tickets are High or Critical severity?
4. Which teams have the highest escalation workload?
5. How many tickets require human review?
6. Where is the model least confident?
7. Which categories may need better taxonomy, reviewer training, or model improvement?
8. What should leaders prioritise operationally?

The dashboard is designed for operational leaders, Trust & Safety reviewers, QA analysts, policy teams, and AI operations teams.

## Dataset Used

```text
data/synthetic_user_reports.csv
```

Optional enriched dataset:

```text
data/synthetic_user_reports_with_summaries.csv
```

## Dashboard Audience

| Audience | What They Need |
|---|---|
| Trust & Safety Operations Lead | Overall workload, urgent tickets, escalation pressure, SLA priorities |
| Reviewer Team Lead | Queue priorities, human review demand, high-risk categories |
| QA Analyst | Low-confidence cases, category errors, severity distribution, review sampling |
| Policy Specialist | Misinformation, policy confusion, appeal patterns, taxonomy gaps |
| AI Operations Analyst | Model confidence, low-confidence categories, automation risk |
| Executive Stakeholder | High-level operational risk, workload summary, responsible AI safeguards |

## Dashboard Layout

Recommended dashboard title:

```text
AI Trust & Safety Risk Triage Dashboard
```

Recommended subtitle:

```text
Synthetic user report analysis for risk classification, escalation, human review, and responsible AI monitoring
```

The dashboard should have four main sections:

1. Executive overview
2. Risk and severity analysis
3. Escalation and human review workload
4. Model confidence and responsible AI monitoring

## Section 1: Executive Overview

This section should appear at the top of the dashboard.

### KPI Cards

| KPI Card | Field / Calculation | Why It Matters |
|---|---|---|
| Total tickets | Count of ticket_id | Shows total workload |
| High + Critical tickets | Count where severity is High or Critical | Shows urgent operational demand |
| Human review required | Count where human_review_required is True | Shows reviewer workload |
| Human review rate | Human review tickets / total tickets | Shows reliance on manual review |
| Average model confidence | Average of model_confidence | Shows overall classifier confidence |
| Low-confidence tickets | Count where model_confidence < 0.75 | Shows automation uncertainty |
| Critical tickets | Count where severity = Critical | Shows most urgent safety risk |
| Number of escalation teams | Count distinct escalation_team | Shows operational spread |

### Recommended KPI Wording

| KPI | Display Label |
|---|---|
| total_tickets | Total Tickets |
| urgent_tickets | High + Critical Tickets |
| human_review_tickets | Human Review Required |
| human_review_rate | Human Review Rate |
| avg_model_confidence | Avg Model Confidence |
| low_confidence_tickets | Low-Confidence Tickets |
| critical_tickets | Critical Tickets |
| escalation_teams | Escalation Teams |

## Section 2: Risk and Severity Analysis

This section explains what types of risks are appearing in the ticket queue.

### Visual 1: Tickets by Risk Category

| Setting | Recommendation |
|---|---|
| Chart type | Horizontal bar chart |
| X-axis | Ticket count |
| Y-axis | Risk category |
| Sort | Descending by ticket count |
| Purpose | Show the most common risk categories |

Insight this visual should support:

```text
Which Trust & Safety risk categories create the largest volume of user reports?
```

### Visual 2: Tickets by Severity

| Setting | Recommendation |
|---|---|
| Chart type | Bar chart |
| X-axis | Severity |
| Y-axis | Ticket count |
| Sort | Critical, High, Medium, Low |
| Purpose | Show urgency distribution |

Insight this visual should support:

```text
How much of the queue requires urgent or specialist attention?
```

### Visual 3: Severity by Risk Category

| Setting | Recommendation |
|---|---|
| Chart type | Stacked bar chart or heatmap |
| X-axis | Risk category |
| Y-axis | Ticket count |
| Legend | Severity |
| Purpose | Show which categories contain the most High and Critical cases |

Insight this visual should support:

```text
Which risk categories drive the most urgent workload?
```

## Section 3: Escalation and Human Review Workload

This section shows operational routing pressure.

### Visual 4: Escalation Team Workload

| Setting | Recommendation |
|---|---|
| Chart type | Horizontal bar chart |
| X-axis | Ticket count |
| Y-axis | Escalation team |
| Sort | Descending by ticket count |
| Purpose | Show team workload distribution |

Insight this visual should support:

```text
Which teams receive the highest volume of escalated tickets?
```

### Visual 5: Human Review Rate by Risk Category

| Setting | Recommendation |
|---|---|
| Chart type | Horizontal bar chart |
| X-axis | Human review rate percentage |
| Y-axis | Risk category |
| Sort | Descending by human review rate |
| Purpose | Show where manual judgement is most required |

Insight this visual should support:

```text
Which categories rely most heavily on human review?
```

### Visual 6: Final Action Distribution

| Setting | Recommendation |
|---|---|
| Chart type | Horizontal bar chart |
| X-axis | Ticket count |
| Y-axis | Final action |
| Sort | Descending by ticket count |
| Purpose | Show operational outcomes |

Insight this visual should support:

```text
What actions are most commonly taken after triage?
```

## Section 4: Model Confidence and Responsible AI Monitoring

This section shows where automation may be weaker or require stronger oversight.

### Visual 7: Average Model Confidence by Risk Category

| Setting | Recommendation |
|---|---|
| Chart type | Horizontal bar chart |
| X-axis | Average model confidence |
| Y-axis | Risk category |
| Sort | Ascending by model confidence |
| Purpose | Highlight categories where model confidence is lowest |

Insight this visual should support:

```text
Which categories may need better training data, taxonomy clarification, or reviewer oversight?
```

### Visual 8: Low-Confidence Tickets by Risk Category

| Setting | Recommendation |
|---|---|
| Chart type | Bar chart |
| X-axis | Risk category |
| Y-axis | Count of tickets where model_confidence < 0.75 |
| Purpose | Show where automation uncertainty is concentrated |

Insight this visual should support:

```text
Where should human review and model improvement efforts focus?
```

### Visual 9: Human Review Required vs Not Required

| Setting | Recommendation |
|---|---|
| Chart type | Donut chart or simple bar chart |
| Field | human_review_required |
| Purpose | Show proportion of tickets requiring human review |

Insight this visual should support:

```text
How much of the queue should not be handled by automation alone?
```

## Suggested Dashboard Filters

The dashboard should include filters for:

| Filter | Field |
|---|---|
| Date range | created_at |
| Risk category | risk_category |
| Severity | severity |
| Escalation team | escalation_team |
| Human review required | human_review_required |
| Region | region |
| Channel | channel |
| Language | language |

## Suggested Dashboard Pages

If building the dashboard in Power BI, Tableau, Looker Studio, or Flourish, use these pages:

| Page | Purpose |
|---|---|
| Executive Overview | KPIs and top-level summary |
| Risk Analysis | Category, subcategory, and severity patterns |
| Escalation Workload | Team routing and urgent queue demand |
| Responsible AI Monitoring | Model confidence, low-confidence cases, human review |
| QA and Improvement | Suggested QA sample, review rates, process improvement areas |

## Priority Queue Table

The dashboard should include a table showing the highest-priority tickets.

Recommended columns:

| Column | Purpose |
|---|---|
| ticket_id | Unique ticket reference |
| created_at | Ticket creation date |
| risk_category | Primary risk category |
| subcategory | More specific risk type |
| severity | Urgency level |
| sla_target_hours | SLA target |
| model_confidence | Automation confidence |
| escalation_team | Responsible team |
| human_review_required | Human review flag |
| final_action | Recommended or completed action |
| user_report | Original synthetic user report |

Recommended sort order:

1. Critical severity
2. High severity
3. Low model confidence
4. Oldest created date

## Responsible AI Dashboard Checks

The dashboard should help monitor responsible AI safeguards.

| Check | Dashboard Logic |
|---|---|
| High and Critical cases require human review | Filter severity High/Critical and check human_review_required |
| Low-confidence tickets require human review | Filter model_confidence < 0.75 |
| Sensitive categories are escalated | Filter child safety, self-harm, privacy, fraud |
| Model confidence is monitored by category | Average model_confidence by risk_category |
| Human review demand is visible | Human review rate KPI and chart |
| Specialist team workload is visible | Escalation team workload chart |
| Urgent cases are prioritised | Priority queue table |

## Suggested Dashboard Insights

The final dashboard should communicate insights such as:

1. High and Critical severity tickets create the most urgent operational workload.
2. Sensitive categories require mandatory human review.
3. Low-confidence model predictions should be routed to human reviewers.
4. Escalation team workload can help identify specialist capacity needs.
5. Model confidence by category can highlight where the classifier may need improvement.
6. Human review is a responsible AI safeguard, not just an operational cost.
7. Synthetic data allows safe public demonstration without exposing real user information.

## Example Executive Summary Text

This dashboard analyses 500 fully synthetic Trust & Safety user reports. It shows how incoming reports can be categorised by risk type, prioritised by severity, routed to escalation teams, and monitored through responsible AI safeguards.

The dashboard highlights urgent High and Critical tickets, human review demand, escalation team workload, and model confidence patterns. It demonstrates how AI-assisted triage can support reviewer workflows while keeping humans responsible for sensitive, ambiguous, and high-impact decisions.

## Dashboard Design Principles

| Principle | Recommendation |
|---|---|
| Keep KPIs visible | Place the most important operational metrics at the top |
| Prioritise risk | Show severity and urgent tickets early |
| Support action | Include escalation team and priority queue views |
| Make AI uncertainty visible | Show low-confidence tickets and confidence by category |
| Keep responsible AI central | Show human review and safeguard checks clearly |
| Avoid clutter | Use simple charts with clear labels |
| Make it recruiter-friendly | Use clean titles and short explanatory notes |

## Suggested Visual Style

Recommended design:

| Element | Recommendation |
|---|---|
| Background | Clean and light |
| Fonts | Simple and readable |
| Chart style | Minimal, professional, easy to scan |
| Labels | Clear, human-readable labels |
| Colours | Use consistent severity colours if possible |
| Layout | KPI cards at top, charts below, priority table at bottom |
| Notes | Add short interpretation notes under key visuals |

Suggested severity colour logic:

| Severity | Suggested Colour Meaning |
|---|---|
| Critical | Highest urgency |
| High | Serious risk |
| Medium | Moderate risk |
| Low | Standard support priority |

Avoid using too many colours. The dashboard should feel calm, professional, and operational.

## Recommended Dashboard Screenshot Names

If screenshots are added later, save them as:

```text
images/dashboard_overview.png
images/dashboard_risk_analysis.png
images/dashboard_escalation_workload.png
images/dashboard_responsible_ai_monitoring.png
```

## Portfolio README Placement

The README should include a dashboard section like this:

```markdown
## Dashboard Design

The dashboard monitors synthetic Trust & Safety user reports across risk category, severity, human review requirement, escalation team workload, and model confidence.

Key dashboard views include:

- executive KPI overview
- tickets by risk category
- tickets by severity
- escalation team workload
- human review rate by category
- average model confidence by category
- priority review queue

The dashboard is designed to show how AI-assisted triage can support operational decision-making while keeping responsible AI safeguards visible.
```

## Possible Tools

This dashboard could be built in:

| Tool | Why It Works |
|---|---|
| Power BI | Strong for business dashboards and recruiter-friendly screenshots |
| Tableau Public | Good for public interactive portfolio dashboards |
| Looker Studio | Easy to share and connect to Google Sheets |
| Flourish | Good for simple public visual storytelling |
| Python / Matplotlib | Good for reproducible static charts |
| Streamlit | Good for an interactive Python portfolio app |

## Recommended Tool for This Project

Best option for a polished portfolio:

```text
Power BI or Tableau Public
```

Best option for a fully code-based GitHub project:

```text
Python-generated charts plus dashboard notes
```

Best option for future improvement:

```text
Streamlit app
```

## Dashboard Success Criteria

The dashboard is successful if a recruiter or hiring manager can quickly understand:

| Question | Answered By |
|---|---|
| What problem does this project solve? | Executive summary and KPIs |
| What risks are being triaged? | Risk category chart |
| How urgent is the workload? | Severity chart and High/Critical KPIs |
| Where is human judgement required? | Human review KPI and chart |
| How is AI being used responsibly? | Model confidence and responsible AI checks |
| What operational decisions can be made? | Escalation workload and priority queue |
| Is the project safe to share publicly? | Synthetic data notes |

## Limitations

This dashboard is based on synthetic data. It is designed to demonstrate workflow design, analytics thinking, and responsible AI monitoring.

Limitations include:

- ticket patterns are synthetic
- model confidence values are simulated
- no real SLA completion data is included yet
- no resolved_at field is currently available
- no real reviewer QA outcomes are included yet
- no production moderation policy is implemented
- no real user data is used

Future versions could include:

- simulated resolved_at timestamps
- SLA met / missed field
- QA score
- human override indicator
- reviewer decision field
- model prediction vs human final label comparison
- interactive dashboard app

## Portfolio Relevance

This dashboard plan demonstrates skills in:

- business intelligence planning
- Trust & Safety operations analytics
- risk triage monitoring
- KPI design
- responsible AI dashboarding
- human-in-the-loop workflow monitoring
- escalation workload analysis
- model confidence monitoring
- data storytelling
- executive reporting

## Notes

This dashboard plan is for portfolio and educational purposes only. It is not a production Trust & Safety monitoring system.
