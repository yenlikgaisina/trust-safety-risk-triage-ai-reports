# Risk Taxonomy

**Project:** Trust & Safety Operations — AI User Report Triage  
**Version:** 1.0  
**Last Updated:** 2026-05-21  
**Owner:** Trust & Safety Operations

---

## Overview

This document defines the canonical risk taxonomy used to classify user-generated reports submitted to the AI-assisted Trust & Safety triage pipeline. Each report is assigned a **primary risk category**, a **sub-category**, and a **severity tier** to ensure consistent routing, prioritization, and policy enforcement across review queues.

The taxonomy is designed to be exhaustive, mutually exclusive at the primary-category level, and extensible as new harm vectors emerge.

---

## Primary Risk Categories

### 1. Harmful Content

Reports in this category involve user-generated content that poses a direct risk of physical, psychological, or social harm to individuals or groups.

| Sub-Category | Description | Example Signals |
|---|---|---|
| Violence & Threats | Explicit or credible threats of violence against identified or identifiable persons | Weapon references, target specificity |
| Hate Speech | Content that attacks a protected class based on race, ethnicity, religion, gender, sexual orientation, disability, or national origin | Slurs, dehumanizing language, calls for discrimination |
| Self-Harm & Suicide | Content that promotes, glorifies, or provides methods for self-injury or suicide | Method details, encouragement, pacts |
| Child Safety (CSAM/CSEM) | Any content that sexually exploits or endangers minors | Age indicators, explicit material, grooming patterns |
| Graphic Violence | Gore, torture, or gratuitous depictions of injury without clear journalistic or educational context | Shock content, snuff imagery |

**Default Severity Floor:** Tier 3 (High) — escalate immediately if CSAM/CSEM indicators present.

---

### 2. Harassment & Abuse

Reports involving targeted interpersonal misconduct directed at a specific individual or group.

| Sub-Category | Description | Example Signals |
|---|---|---|
| Targeted Harassment | Sustained, repeated hostile contact with a specific user | Multiple reports from same target, coordinated pile-ons |
| Doxxing | Publication or threat to publish private personally identifiable information (PII) | Home addresses, phone numbers, employer details |
| Sexual Harassment | Unwanted sexual advances, explicit messages, or non-consensual intimate imagery (NCII) | Unsolicited explicit content, sextortion |
| Impersonation | Falsely assuming the identity of another person or organization to deceive | Cloned profiles, misleading handles |
| Stalking | Persistent unwanted contact or monitoring behavior that induces fear | Repeated check-ins, location references, fear statements from target |

**Default Severity Floor:** Tier 2 (Medium) — escalate to Tier 3 if PII exposed or physical threat implied.

---

### 3. Misinformation & Manipulation

Reports involving deceptive content that undermines informed decision-making, public discourse, or democratic processes.

| Sub-Category | Description | Example Signals |
|---|---|---|
| Health Misinformation | False or unverified medical claims that could cause harm if acted upon | Vaccine misinformation, miracle cures, denial of established medical consensus |
| Election Interference | Content designed to suppress votes, spread false electoral information, or impersonate electoral authorities | False polling dates, voter ID disinformation |
| Synthetic Media / Deepfakes | AI-generated or manipulated audio/video misrepresenting real persons | Unconsented face-swap, voice clone of public figure |
| Coordinated Inauthentic Behavior | Organized campaigns using fake accounts to amplify narratives | Identical post patterns, bot-like activity, coordinated timing |
| Scams & Fraud | Content designed to deceive users into financial loss or credential theft | Phishing links, advance-fee schemes, impersonation of financial institutions |

**Default Severity Floor:** Tier 2 (Medium) — escalate Election Interference and CSAM-adjacent synthetic media to Tier 3.

---

### 4. Platform Integrity

Reports involving violations of platform rules that do not necessarily involve direct harm but undermine the integrity of the service.

| Sub-Category | Description | Example Signals |
|---|---|---|
| Spam | Unsolicited bulk messages, low-quality content, or repetitive promotional material | High message volume, identical content across accounts |
| Account Takeover (ATO) | Evidence of unauthorized access to a user account | Unusual login geography, user reports of unrecognized activity |
| Manipulation of Engagement Metrics | Artificial inflation of likes, followers, views, or ratings | Sudden metric spikes, third-party service references |
| Terms of Service (ToS) Violations | Behavior that violates platform rules without falling into a higher-risk category | Prohibited commercial activity, ban evasion |

**Default Severity Floor:** Tier 1 (Low) — escalate ATO to Tier 2 immediately given account security implications.

---

### 5. Regulatory & Legal Risk

Reports that implicate legal obligations, regulatory compliance, or potential liability for the platform.

| Sub-Category | Description | Example Signals |
|---|---|---|
| Intellectual Property Infringement | Unauthorized use of copyrighted, trademarked, or patented material | DMCA notices, watermarked content, logo misuse |
| Privacy Violations | Processing or publication of personal data without legal basis | GDPR/CCPA subject access requests, unauthorized data sharing |
| Illegal Goods & Services | Facilitation of trade in controlled substances, weapons, or other prohibited items | Drug sale terminology, unlicensed firearms, counterfeit goods |
| Financial Crimes | Money laundering, fraud facilitation, or unauthorized financial services activity | Suspicious transaction patterns, unregulated crypto schemes |

**Default Severity Floor:** Tier 2 (Medium) — Legal team notification required for all Tier 3 regulatory incidents.

---

## Severity Tier Definitions

| Tier | Label | SLA (First Response) | Human Review Required | Description |
|---|---|---|---|---|
| **T1** | Low | 72 hours | No (AI disposition permitted) | Minor policy violations with limited harm potential and no identifiable victim |
| **T2** | Medium | 24 hours | Recommended | Moderate harm potential or policy violation involving an identifiable affected party |
| **T3** | High | 4 hours | **Mandatory** | Imminent harm risk, legal exposure, CSAM/CSEM indicators, or credible physical threat |
| **T4** | Critical | 1 hour | **Mandatory — Senior Escalation** | Active crisis scenario (e.g., imminent violence, CSAM confirmed, coordinated attack on infrastructure) |

---

## Taxonomy Governance

- **Review Cadence:** The taxonomy is reviewed quarterly by the Trust & Safety Policy team and updated to reflect emerging harm vectors, regulatory changes, and post-incident learnings.
- **Change Control:** All taxonomy modifications require sign-off from the Head of Trust & Safety and are logged in the policy change register.
- **Versioning:** Semantic versioning (MAJOR.MINOR.PATCH) is applied. Breaking changes to category codes increment the MAJOR version and trigger re-training of any ML classifiers dependent on this taxonomy.
- **Feedback Loop:** Analyst disagreement rates and escalation override patterns are reviewed monthly to identify taxonomy gaps or ambiguities.

---

## Cross-Reference

| Document | Purpose |
|---|---|
| `docs/escalation_decision_tree.md` | Routing logic based on taxonomy classification |
| `docs/qa_checklist.md` | Quality assurance criteria by risk category |
| `docs/human_in_the_loop_process.md` | Human review triggers and handoff procedures |
| `docs/responsible_ai_safeguards.md` | Model governance and bias mitigation controls |
| `docs/data_dictionary.md` | Field-level definitions for the case management dataset |
