# Escalation Decision Tree

**Project:** Trust & Safety Operations — AI User Report Triage  
**Version:** 1.0  
**Last Updated:** 2026-05-21  
**Owner:** Trust & Safety Operations

---

## Overview

This document defines the structured decision logic used to route, prioritize, and escalate incoming user reports through the AI-assisted triage pipeline. The decision tree is applied sequentially after initial AI classification. Outputs from this process determine queue assignment, SLA clock start, and whether human review is triggered immediately or deferred.

All routing decisions are logged with a `routing_reason_code` to support quality assurance, auditing, and model retraining pipelines.

---

## Stage 1 — Intake & Automated Pre-Screening

Every inbound report enters the pipeline at this stage. The AI pre-screening model evaluates a set of hard-coded trigger conditions before any classifier inference is run.

```
REPORT RECEIVED
     │
     ▼
[1.1] Does the report contain any CSAM/CSEM keyword signals or hash-match hits?
     │
     ├── YES ──► FLAG: CSAM_IMMEDIATE
     │            └── Route to: CSAM Specialist Queue (T4 — 1-hour SLA)
     │                Human review: MANDATORY within 30 minutes
     │                Notify: Legal, Head of T&S, on-call Safety Lead
     │
     └── NO  ──► Continue to Stage 2
```

**Note:** CSAM/CSEM pre-screening runs on every report regardless of submitted category. Hash-matching uses PhotoDNA-equivalent perceptual hashing; keyword matching uses a maintained sensitive-term lexicon reviewed monthly.

---

## Stage 2 — AI Severity Classification

The primary classifier assigns a risk category and severity tier (T1–T4) based on report content, metadata, and reporter history. This output drives all downstream routing.

```
     │
     ▼
[2.1] AI Classifier Output — Severity Tier Assignment
     │
     ├── T4 (Critical) ──► Route to: Crisis Response Queue
     │                      Human review: MANDATORY — Senior Analyst or above
     │                      SLA: 1 hour from report submission
     │                      Parallel action: Notify on-call T&S Lead + Legal
     │
     ├── T3 (High)     ──► Route to: Priority Review Queue
     │                      Human review: MANDATORY
     │                      SLA: 4 hours from report submission
     │                      Continue to Stage 3 (Confidence Check)
     │
     ├── T2 (Medium)   ──► Route to: Standard Review Queue
     │                      Human review: Recommended (see Stage 3)
     │                      SLA: 24 hours from report submission
     │                      Continue to Stage 3 (Confidence Check)
     │
     └── T1 (Low)      ──► Route to: Automated Disposition Queue
                           Human review: Not required (AI may close)
                           SLA: 72 hours from report submission
                           Continue to Stage 4 (AI Auto-Disposition)
```

---

## Stage 3 — Confidence Threshold & Override Logic

For T2 and T3 reports, the classifier confidence score determines whether the AI recommendation is accepted or overridden for mandatory human review.

```
     │ (T2 or T3 reports)
     ▼
[3.1] AI Model Confidence Score ≥ 0.85?
     │
     ├── YES ──► [3.2] Check: Is this the reported user's 3rd+ offense in 90 days?
     │                │
     │                ├── YES ──► Escalate to T3 regardless of original tier
     │                │           Route to: Priority Review Queue
     │                │           Flag: REPEAT_OFFENDER
     │                │
     │                └── NO  ──► Accept AI tier classification
     │                            Route per Stage 2 assignment
     │
     └── NO  ──► Confidence below threshold — mandatory human review
                 Route to: Human Review Queue (tier retained)
                 Flag: LOW_CONFIDENCE_OVERRIDE
                 Analyst must validate or override AI classification
```

---

## Stage 4 — AI Auto-Disposition (T1 Only)

T1 reports with high model confidence may be automatically closed by the AI without human review, subject to the following safety checks.

```
     │ (T1 reports only)
     ▼
[4.1] Is the reporter's account flagged as a trusted reporter or verified organization?
     │
     ├── YES ──► Elevate to T2 — route to Standard Review Queue
     │           (Trusted reporters have elevated signal weight)
     │
     └── NO  ──► [4.2] Has this exact content hash been actioned before (known-bad signal)?
                 │
                 ├── YES ──► Auto-action: apply prior enforcement decision
                 │           Log: AUTO_DISPOSITION_KNOWN_SIGNAL
                 │
                 └── NO  ──► [4.3] AI Confidence Score ≥ 0.90?
                             │
                             ├── YES ──► Auto-close with AI recommendation
                             │           Log: AUTO_DISPOSITION_HIGH_CONFIDENCE
                             │           QA sample: 5% of auto-closed T1 cases reviewed weekly
                             │
                             └── NO  ──► Route to Human Review Queue
                                         Flag: T1_CONFIDENCE_INSUFFICIENT
```

---

## Stage 5 — Human Analyst Review

Reports routed to human review queues follow this structured review process.

```
     │ (Human review queue)
     ▼
[5.1] Analyst reviews report content, AI classification, and account history
     │
     ▼
[5.2] Does the analyst agree with the AI severity classification?
     │
     ├── YES ──► Proceed to enforcement action per policy
     │           Log: ANALYST_CONFIRMED
     │
     └── NO  ──► [5.3] Analyst override — reclassify severity
                 │
                 ├── Upgrade (e.g., T2 → T3) ──► Re-route to higher-tier queue
                 │                                 Log: ANALYST_UPGRADE
                 │                                 Notify: Tier Lead if T3 → T4
                 │
                 └── Downgrade (e.g., T3 → T2) ──► Re-route to standard queue
                                                    Log: ANALYST_DOWNGRADE
                                                    Required: written justification
```

**QA Flag:** Override rates exceeding 15% for any analyst in a given week trigger a calibration review with the QA Lead.

---

## Stage 6 — Enforcement Action & Case Closure

Following human or AI disposition, the enforcement action is applied and the case is closed.

```
     │
     ▼
[6.1] Enforcement Action Applied
     │
     ├── Content Removed
     ├── Account Warning Issued
     ├── Account Suspended (temporary)
     ├── Account Terminated (permanent)
     ├── Report Dismissed (no violation found)
     ├── Referred to Law Enforcement
     └── Escalated to Legal / External Compliance
     │
     ▼
[6.2] Case Closed — record outcome in case management system
     │
     └── [6.3] Post-action: Was reported user previously actioned within 30 days?
                 │
                 ├── YES ──► Flag account for Enhanced Monitoring
                 │           Set: WATCH_LIST = TRUE
                 │
                 └── NO  ──► Standard case closure
                             No additional monitoring required
```

---

## Routing Summary Matrix

| Severity Tier | AI Confidence | Condition | Assigned Queue | Human Review |
|---|---|---|---|---|
| T4 (Critical) | Any | Any | Crisis Response | Mandatory — Senior |
| T3 (High) | ≥ 0.85 | No repeat offense | Priority Review | Mandatory |
| T3 (High) | < 0.85 | Any | Human Review | Mandatory |
| T2 (Medium) | ≥ 0.85 | No repeat offense | Standard Review | Recommended |
| T2 (Medium) | < 0.85 | Any | Human Review | Mandatory |
| T1 (Low) | ≥ 0.90 | No trusted reporter | Automated Disposition | No |
| T1 (Low) | < 0.90 | Any | Human Review | Mandatory |
| Any | Any | CSAM/CSEM signal | CSAM Specialist | Mandatory — Urgent |
| Any | Any | Repeat offender (3+ / 90d) | Priority Review | Mandatory |

---

## Escalation Contacts

| Role | Escalation Trigger |
|---|---|
| T&S Tier Lead | Any T3 case flagged REPEAT_OFFENDER or analyst override to T4 |
| Head of Trust & Safety | Any T4 case; CSAM confirmed; coordinated attack signals |
| Legal Counsel | Regulatory or legal risk category at T3+; all CSAM referrals |
| Law Enforcement Liaison | Credible imminent physical threat; confirmed CSAM |
| Communications / PR | Coordinated inauthentic behavior campaigns at scale; high-media-risk incidents |

---

## Cross-Reference

| Document | Purpose |
|---|---|
| `docs/risk_taxonomy.md` | Category and severity tier definitions |
| `docs/qa_checklist.md` | Quality criteria applied at Stage 5 |
| `docs/human_in_the_loop_process.md` | Detailed human review procedures |
| `docs/responsible_ai_safeguards.md` | Model confidence thresholds and bias controls |
| `docs/data_dictionary.md` | Field definitions for routing_reason_code and flag fields |
