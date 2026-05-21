# QA Checklist — Trust & Safety AI Triage Operations

**Project:** Trust & Safety Operations — AI User Report Triage  
**Version:** 1.0  
**Last Updated:** 2026-05-21  
**Owner:** Trust & Safety QA Lead

---

## Overview

This checklist defines the quality assurance criteria applied to human analyst reviews within the AI-assisted triage pipeline. It is used in three contexts:

1. **Ongoing case review** — applied by analysts during active case work
2. **QA audits** — applied by the QA Lead during weekly random sample reviews
3. **Calibration sessions** — used as a structured rubric in analyst calibration exercises

Checklists are recorded per case in the case management system under `qa_review_log`. Defect codes are used to track systemic quality issues and feed into model retraining and policy clarification cycles.

---

## Section 1 — Report Intake & Classification Quality

These checks verify that the incoming report was correctly received, categorized, and assigned.

| # | Check | Pass Criteria | Defect Code |
|---|---|---|---|
| 1.1 | Report completeness | All required intake fields present (reporter ID, timestamp, content reference, report category) | QA-INT-001 |
| 1.2 | AI classification accuracy | AI-assigned risk category aligns with policy definitions in `risk_taxonomy.md` | QA-INT-002 |
| 1.3 | Severity tier appropriateness | Assigned severity tier (T1–T4) matches harm potential per taxonomy severity floor rules | QA-INT-003 |
| 1.4 | SLA clock initiation | Case SLA timer started within 5 minutes of report submission timestamp | QA-INT-004 |
| 1.5 | Duplicate detection | No duplicate report exists for the same content within the preceding 72-hour window | QA-INT-005 |
| 1.6 | Sub-category specificity | AI sub-category label is the most specific applicable label, not a catch-all default | QA-INT-006 |

---

## Section 2 — Content Review Quality

These checks verify that the analyst performed a thorough and policy-compliant review of the reported content.

| # | Check | Pass Criteria | Defect Code |
|---|---|---|---|
| 2.1 | Full content reviewed | Analyst reviewed the complete reported content, not just a summary or excerpt | QA-CNT-001 |
| 2.2 | Context considered | Analyst reviewed account history, prior reports, and contextual metadata before making a determination | QA-CNT-002 |
| 2.3 | Policy applied correctly | Enforcement decision is supported by a specific, cited policy clause — not general judgment | QA-CNT-003 |
| 2.4 | Borderline content escalated | Content meeting any borderline escalation trigger (see `escalation_decision_tree.md` Stage 3) was escalated rather than dismissed | QA-CNT-004 |
| 2.5 | Protected class review | If hate speech sub-category is present, analyst confirmed whether a protected characteristic is targeted | QA-CNT-005 |
| 2.6 | Threat credibility assessment | For Violence & Threats sub-category, analyst documented their assessment of threat credibility (speculative vs. credible) | QA-CNT-006 |
| 2.7 | CSAM/CSEM handling | If any CSAM/CSEM indicator was present at any point in the review, the case was immediately escalated per Stage 1 protocol | QA-CNT-007 |

---

## Section 3 — Decision & Enforcement Quality

These checks verify that the enforcement action taken was proportionate, consistent, and correctly documented.

| # | Check | Pass Criteria | Defect Code |
|---|---|---|---|
| 3.1 | Enforcement action proportionate | Action taken (warn / suspend / terminate / dismiss) is proportionate to violation severity per enforcement matrix | QA-DEC-001 |
| 3.2 | First-offense consideration | For first-offense T2 violations, warning was considered before suspension unless policy mandates otherwise | QA-DEC-002 |
| 3.3 | Repeat offender escalation | If reported user has 2+ prior enforcements in 90 days, enhanced action was applied or documented rationale provided for standard action | QA-DEC-003 |
| 3.4 | AI override documented | If analyst overrode AI classification or recommendation, a written justification is present in the case record | QA-DEC-004 |
| 3.5 | False positive check | If report was dismissed, analyst confirmed the dismissal is not a false negative (i.e., actual violation missed) | QA-DEC-005 |
| 3.6 | Legal/regulatory flag applied | Cases involving potential legal or regulatory exposure are flagged with `legal_flag = TRUE` and Legal team notified | QA-DEC-006 |
| 3.7 | Action applied correctly | Enforcement action was correctly executed in the platform tooling (e.g., content removed, account status updated) | QA-DEC-007 |

---

## Section 4 — Documentation & Audit Trail

These checks verify that the case record is complete, accurate, and auditable.

| # | Check | Pass Criteria | Defect Code |
|---|---|---|---|
| 4.1 | Case notes present | A minimum of one substantive analyst note is present, describing the basis for the enforcement decision | QA-DOC-001 |
| 4.2 | Timestamps accurate | All system-generated and analyst-entered timestamps are internally consistent and within expected ranges | QA-DOC-002 |
| 4.3 | Routing reason code set | `routing_reason_code` field is populated with the correct value per the escalation decision tree | QA-DOC-003 |
| 4.4 | Outcome code set | `outcome_code` field is populated with the correct enforcement outcome value | QA-DOC-004 |
| 4.5 | SLA compliance recorded | Case closed within the SLA window for its assigned tier, or SLA breach recorded with documented reason | QA-DOC-005 |
| 4.6 | Sensitive case flagging | Cases involving vulnerable users (minors, self-harm indicators, domestic violence signals) are flagged with `sensitive_case = TRUE` | QA-DOC-006 |
| 4.7 | QA review log entry | This QA checklist completion is recorded in `qa_review_log` with analyst ID, QA reviewer ID, date, and pass/fail per section | QA-DOC-007 |

---

## Section 5 — Bias & Consistency Checks (QA Audit Use Only)

These checks are applied by the QA Lead during structured audits and calibration sessions. They are not required for every case review.

| # | Check | Pass Criteria | Defect Code |
|---|---|---|---|
| 5.1 | Consistent application across demographics | Enforcement decisions for comparable violations do not vary by apparent protected characteristic of the reported user | QA-BIAS-001 |
| 5.2 | Consistent application across regions | Enforcement decisions are consistent regardless of the geographic origin of the report or reported content | QA-BIAS-002 |
| 5.3 | AI confidence vs. analyst agreement correlation | For T2/T3 cases, analyst override rate is within ±5% of the team baseline for the same risk category | QA-BIAS-003 |
| 5.4 | Language/translation quality | For reports in non-English languages, translation quality did not materially affect the classification outcome | QA-BIAS-004 |
| 5.5 | Sentiment-neutral review | Case notes contain objective, policy-based language — not editorializing or emotionally charged commentary | QA-BIAS-005 |

---

## Scoring & Defect Thresholds

QA reviews are scored on a per-section basis. A case passes QA if it meets all mandatory checks (Sections 1–4). Bias checks (Section 5) are scored separately at the analyst level over a rolling 30-day period.

| Score | Definition | Action |
|---|---|---|
| **Pass** | All mandatory checks satisfied | No action required |
| **Minor Defect** | 1–2 defects in Sections 1–4, none in Section 2.7 or 3.6 | Analyst notified; defect logged |
| **Major Defect** | 3+ defects in Sections 1–4, or any defect in 2.7 or 3.6 | Case reviewed by Tier Lead; analyst coaching scheduled |
| **Critical Defect** | CSAM not escalated; legal flag missed on T3+ case; enforcement action not executed | Immediate escalation to Head of T&S; root cause analysis required |

**Monthly thresholds:** An analyst accumulating more than 10% major defect rate across QA-sampled cases in a calendar month is placed on a performance improvement plan.

---

## QA Sampling Rates

| Queue | Sampling Rate | Reviewer |
|---|---|---|
| Automated Disposition (T1 auto-closed) | 5% random sample weekly | QA Analyst |
| Standard Review Queue (T2) | 10% random sample weekly | QA Analyst |
| Priority Review Queue (T3) | 25% random sample weekly | QA Lead |
| Crisis Response Queue (T4) | 100% post-incident review | Head of T&S + QA Lead |
| CSAM Specialist Queue | 100% supervisory review | CSAM Specialist Lead |

---

## Cross-Reference

| Document | Purpose |
|---|---|
| `docs/risk_taxonomy.md` | Category definitions referenced in Sections 1–2 |
| `docs/escalation_decision_tree.md` | Routing logic referenced in Sections 1–3 |
| `docs/human_in_the_loop_process.md` | Analyst review procedures governing Section 2–3 |
| `docs/responsible_ai_safeguards.md` | Bias and fairness controls referenced in Section 5 |
| `docs/data_dictionary.md` | Definitions for qa_review_log, outcome_code, routing_reason_code fields |
