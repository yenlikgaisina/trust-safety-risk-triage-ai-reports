"""
Risk Category Classifier
Project: AI Trust & Safety Operations Case Study

This script trains a simple text classification model to predict the risk category
of a synthetic Trust & Safety user report.

Model:
- TF-IDF vectorisation
- Logistic Regression classifier

Dataset: data/synthetic_user_reports.csv

Outputs:
- reports/risk_classifier_summary.md
- images/risk_classifier_confusion_matrix.png
- models/risk_classifier_pipeline.joblib

Important:
This model is trained on synthetic data only. It is designed for portfolio
demonstration and should not be treated as production-ready.
"""

from pathlib import Path
import warnings

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


warnings.filterwarnings("ignore", category=UndefinedMetricWarning)


# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "synthetic_user_reports.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"
IMAGES_DIR = PROJECT_ROOT / "images"
MODELS_DIR = PROJECT_ROOT / "models"

REPORT_PATH = REPORTS_DIR / "risk_classifier_summary.md"
CONFUSION_MATRIX_PATH = IMAGES_DIR / "risk_classifier_confusion_matrix.png"
MODEL_PATH = MODELS_DIR / "risk_classifier_pipeline.joblib"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. Load data
# ------------------------------------------------------------

def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the synthetic ticket dataset."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at: {path}")

    df = pd.read_csv(path)

    required_columns = ["ticket_id", "user_report", "risk_category"]

    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df = df.dropna(subset=["user_report", "risk_category"]).copy()

    df["user_report"] = df["user_report"].astype(str)
    df["risk_category"] = df["risk_category"].astype(str)

    return df


df = load_data(DATA_PATH)


# ------------------------------------------------------------
# 3. Prepare features and labels
# ------------------------------------------------------------

X = df["user_report"]
y = df["risk_category"]

class_counts = y.value_counts()
use_stratify = class_counts.min() >= 2

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y if use_stratify else None,
)


# ------------------------------------------------------------
# 4. Build model pipeline
# ------------------------------------------------------------

model = Pipeline(
    steps=[
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2),
                min_df=2,
                max_features=5000,
            ),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42,
            ),
        ),
    ]
)


# ------------------------------------------------------------
# 5. Train model
# ------------------------------------------------------------

model.fit(X_train, y_train)


# ------------------------------------------------------------
# 6. Evaluate model
# ------------------------------------------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

report_dict = classification_report(
    y_test,
    y_pred,
    output_dict=True,
    zero_division=0,
)

report_text = classification_report(
    y_test,
    y_pred,
    zero_division=0,
)

labels = sorted(y.unique())

conf_matrix = confusion_matrix(y_test, y_pred, labels=labels)

plt.figure(figsize=(12, 10))
display = ConfusionMatrixDisplay(
    confusion_matrix=conf_matrix,
    display_labels=labels,
)
display.plot(
    xticks_rotation=90,
    values_format="d",
)
plt.title("Risk Category Classifier Confusion Matrix")
plt.tight_layout()
plt.savefig(CONFUSION_MATRIX_PATH, dpi=300)
plt.close()


# ------------------------------------------------------------
# 7. Extract top features by class
# ------------------------------------------------------------

def get_top_features_by_class(pipeline: Pipeline, top_n: int = 10) -> pd.DataFrame:
    """Extract top positive TF-IDF features for each class."""
    vectorizer = pipeline.named_steps["tfidf"]
    classifier = pipeline.named_steps["classifier"]

    feature_names = vectorizer.get_feature_names_out()
    classes = classifier.classes_

    rows = []

    for class_index, class_name in enumerate(classes):
        coefficients = classifier.coef_[class_index]
        top_indices = coefficients.argsort()[-top_n:][::-1]

        for rank, feature_index in enumerate(top_indices, start=1):
            rows.append(
                {
                    "risk_category": class_name,
                    "rank": rank,
                    "feature": feature_names[feature_index],
                    "coefficient": round(float(coefficients[feature_index]), 4),
                }
            )

    return pd.DataFrame(rows)


top_features = get_top_features_by_class(model, top_n=10)


# ------------------------------------------------------------
# 8. Example predictions
# ------------------------------------------------------------

example_reports = [
    "Someone changed my password and I cannot access my account.",
    "A user keeps sending me threatening messages.",
    "I am worried an adult is contacting my younger sibling.",
    "This account is asking people to send money through a private link.",
    "A user posted my phone number publicly.",
    "I do not understand why my post was removed.",
]

example_predictions = []

for report in example_reports:
    predicted_category = model.predict([report])[0]

    if hasattr(model.named_steps["classifier"], "predict_proba"):
        probabilities = model.predict_proba([report])[0]
        confidence = probabilities.max()
    else:
        confidence = None

    example_predictions.append(
        {
            "user_report": report,
            "predicted_risk_category": predicted_category,
            "model_confidence": round(float(confidence), 3)
            if confidence is not None
            else "Not available",
        }
    )

example_predictions_df = pd.DataFrame(example_predictions)


# ------------------------------------------------------------
# 9. Convert tables to markdown
# ------------------------------------------------------------

def dataframe_to_markdown(data: pd.DataFrame) -> str:
    """Convert a DataFrame to markdown without the index."""
    return data.to_markdown(index=False)


classification_report_df = (
    pd.DataFrame(report_dict)
    .transpose()
    .reset_index()
    .rename(columns={"index": "class_or_metric"})
)

for column in ["precision", "recall", "f1-score", "support"]:
    if column in classification_report_df.columns:
        classification_report_df[column] = classification_report_df[column].round(3)


# ------------------------------------------------------------
# 10. Write markdown report
# ------------------------------------------------------------

summary_report = f"""# Risk Classifier Summary

## Project Context

This report is part of the portfolio project:

**AI Trust & Safety Operations Case Study: Risk Triage, Taxonomy Design and Escalation Workflow**

The classifier uses synthetic user reports to predict the primary Trust & Safety risk category.

No real users, platforms, accounts, companies, or incidents are included.

## Model Objective

The objective is to predict:

```text
risk_category
```

from:

```text
user_report
```

This demonstrates how a simple machine learning model can support an AI-assisted triage workflow.

## Model Used

| Component | Method |
|---|---|
| Text representation | TF-IDF |
| Classifier | Logistic Regression |
| Train/test split | 75% train / 25% test |
| Class weighting | Balanced |
| Random seed | 42 |

## Dataset Summary

| Metric | Value |
|---|---|
| Total records used | {len(df)} |
| Training records | {len(X_train)} |
| Test records | {len(X_test)} |
| Number of risk categories | {y.nunique()} |
| Stratified split used | {use_stratify} |

## Risk Category Distribution

{dataframe_to_markdown(class_counts.rename_axis("risk_category").reset_index(name="ticket_count"))}

## Overall Performance

| Metric | Value |
|---|---|
| Accuracy | {round(float(accuracy), 3)} |

## Classification Report

{dataframe_to_markdown(classification_report_df)}

## Confusion Matrix

The confusion matrix chart has been saved here:

```text
images/risk_classifier_confusion_matrix.png
```

## Example Predictions

{dataframe_to_markdown(example_predictions_df)}

## Top Predictive Features by Category

The table below shows the highest-weighted TF-IDF features for each risk category.

{dataframe_to_markdown(top_features)}

## Interpretation

This classifier is useful as a portfolio demonstration of AI-assisted triage.

It shows how unstructured user reports can be converted into structured risk categories using a simple NLP pipeline.

In a Trust & Safety operations setting, this type of model could help:

- pre-classify incoming reports
- prioritise queues
- identify likely escalation paths
- support reviewer decision-making
- detect categories where automation may be uncertain
- create structured inputs for dashboards and QA review

## Responsible AI Safeguards

This model should not make final decisions in high-impact cases.

Human review should be required when:

- the predicted severity is High or Critical
- the report may involve a minor
- the report suggests self-harm or immediate safety risk
- the report involves fraud or account compromise
- the report involves privacy or personal data exposure
- model confidence is low
- the case is ambiguous
- the decision could significantly affect user access, safety, or rights

## Limitations

This model has important limitations:

- the dataset is synthetic
- repeated templates may make classification easier than real-world data
- real user reports are usually messier and more ambiguous
- model performance may not generalise to production data
- the model does not understand policy context deeply
- confidence scores should not be treated as certainty
- the model should support human reviewers, not replace them

## Portfolio Relevance

This script demonstrates skills in:

- text classification
- TF-IDF vectorisation
- logistic regression
- model evaluation
- confusion matrix analysis
- feature interpretation
- responsible AI thinking
- human-in-the-loop workflow design
- Trust & Safety operations analytics

## Notes

This classifier is for portfolio and educational purposes only. It is not production-ready and should not be used for real Trust & Safety decisions.
"""

REPORT_PATH.write_text(summary_report, encoding="utf-8")


# ------------------------------------------------------------
# 11. Save model
# ------------------------------------------------------------

joblib.dump(model, MODEL_PATH)


# ------------------------------------------------------------
# 12. Print results
# ------------------------------------------------------------

print("Risk classifier training complete.")
print(f"Records used: {len(df)}")
print(f"Training records: {len(X_train)}")
print(f"Test records: {len(X_test)}")
print(f"Accuracy: {round(float(accuracy), 3)}")
print(f"Report saved to: {REPORT_PATH}")
print(f"Confusion matrix saved to: {CONFUSION_MATRIX_PATH}")
print(f"Model saved to: {MODEL_PATH}")

print("\nClassification report:")
print(report_text)
