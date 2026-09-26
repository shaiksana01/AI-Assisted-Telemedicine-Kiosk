"""
Machine Learning Training Pipeline for AI-Assisted Telemedicine Triage Model.
Uses RandomForestClassifier on the prototype symptom dataset.
Computes and records genuine calculated evaluation metrics without hardcoded assumptions.
"""

import os
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support
import joblib

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "symptoms.csv")
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
MODEL_PATH = os.path.join(MODELS_DIR, "triage_model.pkl")
METRICS_PATH = os.path.join(MODELS_DIR, "model_metrics.json")

SYMPTOM_COLUMNS = [
    "fever",
    "cough",
    "cold",
    "headache",
    "body_pain",
    "fatigue",
    "sore_throat",
    "vomiting",
    "diarrhea",
    "abdominal_pain",
    "dizziness",
    "chest_pain",
    "breathing_difficulty",
    "high_fever",
    "loss_of_consciousness",
    "severe_bleeding"
]

TARGET_COLUMN = "triage_priority"

def train_and_evaluate():
    """Train Random Forest model and compute real performance metrics."""
    os.makedirs(MODELS_DIR, exist_ok=True)

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Symptom dataset not found at {DATA_PATH}")

    # Load dataset
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded dataset shape: {df.shape}")

    X = df[SYMPTOM_COLUMNS]
    y = df[TARGET_COLUMN]

    # Stratified Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Initialize Random Forest Classifier
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42,
        class_weight="balanced"
    )

    # Perform 5-fold cross-validation on full dataset
    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    cv_scores = cross_val_score(clf, X, y, cv=skf, scoring="accuracy")

    # Fit on training data
    clf.fit(X_train, y_train)

    # Evaluate on holdout test set
    y_pred = clf.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted", zero_division=0)
    
    report_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

    # Fit final model on all data for optimal kiosk deployment
    final_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42,
        class_weight="balanced"
    )
    final_model.fit(X, y)

    # Save artifacts
    model_payload = {
        "model": final_model,
        "feature_names": SYMPTOM_COLUMNS,
        "classes": list(final_model.classes_)
    }
    joblib.dump(model_payload, MODEL_PATH)

    metrics_payload = {
        "model_type": "RandomForestClassifier",
        "dataset_samples": len(df),
        "num_features": len(SYMPTOM_COLUMNS),
        "features": SYMPTOM_COLUMNS,
        "classes": list(final_model.classes_),
        "holdout_test_accuracy": round(float(test_accuracy) * 100, 2),
        "holdout_weighted_f1": round(float(f1) * 100, 2),
        "holdout_weighted_precision": round(float(precision) * 100, 2),
        "holdout_weighted_recall": round(float(recall) * 100, 2),
        "cross_val_accuracy_mean": round(float(cv_scores.mean()) * 100, 2),
        "cross_val_accuracy_std": round(float(cv_scores.std()) * 100, 2),
        "classification_report": report_dict,
        "is_clinically_validated": False,
        "dataset_type": "Educational Prototype Dataset"
    }

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics_payload, f, indent=4)

    print("\n=== REAL MODEL TRAINING & EVALUATION REPORT ===")
    print(f"Dataset Size: {len(df)} samples")
    print(f"Holdout Test Accuracy: {test_accuracy * 100:.2f}%")
    print(f"Holdout Weighted F1-Score: {f1 * 100:.2f}%")
    print(f"Cross-Validation Accuracy (Mean ± Std): {cv_scores.mean()*100:.2f}% ± {cv_scores.std()*100:.2f}%")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Metrics saved to: {METRICS_PATH}")
    print("===============================================\n")

    return metrics_payload

if __name__ == "__main__":
    train_and_evaluate()
