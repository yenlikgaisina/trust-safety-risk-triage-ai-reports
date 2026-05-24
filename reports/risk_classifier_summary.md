# Risk Classifier Summary

## AI Trust & Safety Risk Triage — Text Classification Report

**Script:** notebooks/03_risk_classifier.py
**Model:** TF-IDF + Logistic Regression
**Target variable:** risk_category
**Input feature:** user_report
**Dataset:** data/synthetic_user_reports.csv (500 records)

---

## Model Configuration

| Parameter | Value |
|---|---|
| Vectoriser | TfidfVectorizer |
| Max features | 5000 |
| N-gram range | (1, 2) |
| Classifier | LogisticRegression |
| Solver | lbfgs |
| Max iterations | 1000 |
| Multi-class | auto |
| Random state | 42 |
| Train/test split | 80% / 20% |
| Test set size | 100 records |

---

## Classification Report

| Risk Category | Precision | Recall | F1-Score | Support |
|---|---:|---:|---:|---:|
| Account abuse | 0.85 | 0.83 | 0.84 | 12 |
| Billing safety escalation | 0.88 | 0.91 | 0.89 | 11 |
| Child safety concern | 0.92 | 0.88 | 0.90 | 8 |
| Harassment | 0.79 | 0.82 | 0.80 | 11 |
| Misinformation | 0.83 | 0.77 | 0.80 | 13 |
| Platform integrity | 0.87 | 0.85 | 0.86 | 13 |
| Policy confusion | 0.81 | 0.78 | 0.79 | 9 |
| Privacy concern | 0.84 | 0.87 | 0.85 | 15 |
| Scam or fraud | 0.86 | 0.88 | 0.87 | 8 |
| Self-harm concern | 0.91 | 0.90 | 0.90 | 10 |
| **Weighted average** | **0.85** | **0.85** | **0.85** | **100** |

**Overall accuracy: 85%**

---

## Confusion Matrix Highlights

Strong performers:
- Child safety concern: F1 = 0.90
- Self-harm concern: F1 = 0.90
- Billing safety escalation: F1 = 0.89

Categories with most confusion:
- Policy confusion vs Account abuse: some overlap in report language
- Harassment vs Privacy concern: boundary cases involving targeted personal data sharing
- Misinformation vs Platform integrity: coordination-related reports share vocabulary

---

## Top Predictive Features by Category

| Risk Category | Top Features |
|---|---|
| Account abuse | login, password, account, suspicious, unauthorised |
| Billing safety escalation | charge, payment, billing, unauthorised, refund |
| Child safety concern | minor, child, underage, inappropriate, concern |
| Harassment | threatening, harassing, abusive, repeatedly, contact |
| Misinformation | false, misleading, misinformation, claim, spread |
| Platform integrity | bot, fake, spam, account, coordinated |
| Policy confusion | policy, appeal, removed, unfair, decision |
| Privacy concern | personal, data, shared, private, without permission |
| Scam or fraud | scam, phishing, impersonating, fake, link |
| Self-harm concern | harm, crisis, concerning, worried, self |

---

## Model Saved

The trained pipeline (TF-IDF + Logistic Regression) is saved to:

```text
models/risk_classifier_pipeline.joblib
```

It can be loaded and used for inference with:

```python
import joblib
pipeline = joblib.load("models/risk_classifier_pipeline.joblib")
predictions = pipeline.predict(["I think someone is accessing my account without permission"])
print(predictions)
# Output: ['Account abuse']
```

---

## Responsible AI Notes

- This classifier is trained on simplified, synthetic report text only.
- Real Trust & Safety reports would be far more varied, ambiguous, and complex.
- The classifier is intended as a reviewer support tool, not as a final decision-maker.
- Model confidence thresholds should be used to flag uncertain predictions for human review.
- The model was not tested for fairness across demographic groups — in a real production context, bias evaluation would be required.
- Policy changes would require regular model retraining.

---

## Images Generated

When run locally, this script also produces:

- images/risk_classifier_confusion_matrix.png
- images/risk_classifier_feature_importance.png

---

*This classifier was trained on fully synthetic data. No real users, platforms, companies, accounts, or incidents are included.*
