"""
HealthFit AI Chatbot — Model Training Script

This script trains the NLP intent classification pipeline
from scratch using the intent dataset and saves the trained
artefacts to disk for use at runtime.

Pipeline Trained
----------------
1. Load raw intent data from data/intents.json
2. Extract (pattern, label) pairs
3. Preprocess each pattern (contraction expand, lowercase,
   tokenize, stopword removal, lemmatization)
4. Fit a TF-IDF Vectorizer on all preprocessed patterns
5. Transform patterns into TF-IDF feature vectors
6. Train a Logistic Regression classifier on the vectors
7. Evaluate the model on a held-out test split
8. Print accuracy, precision, recall, and F1-score
9. Save vectorizer → models_ml/tfidf_vectorizer.pkl
10. Save classifier → models_ml/trained_model.pkl

Usage
-----
    python train_model.py

This script should be re-run whenever:
- New intents or patterns are added to intents.json.
- Hyperparameters are changed.
- The preprocessing pipeline is modified.

Model is only retrained if .pkl files do not exist
(automated check at end of this script).
"""

import json
import os
import sys

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
)

# Ensure the project root is on the Python path so that
# imports work regardless of where the script is called from.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from nlp.preprocessor import preprocess_classifier
from config import BaseConfig


# ============================================================
# Path Configuration
# ============================================================

INTENTS_PATH = BaseConfig.INTENTS_PATH
VECTORIZER_PATH = BaseConfig.VECTORIZER_PATH
MODEL_PATH = BaseConfig.CLASSIFIER_PATH
MODEL_DIR = BaseConfig.MODEL_DIR


# ============================================================
# Step 1: Load Intent Data
# ============================================================

def load_intent_data(intents_path: str) -> tuple:
    """Load training patterns and labels from intents.json.

    Iterates through all intents and extracts every pattern
    string paired with its intent tag (label). Patterns with
    empty response lists or no patterns are skipped.

    Parameters
    ----------
    intents_path : str
        Absolute path to the intents.json file.

    Returns
    -------
    tuple[list[str], list[str]]
        A 2-tuple of (patterns, labels) where each pattern
        at index i corresponds to the label at index i.
    """
    print(f"\n[Step 1] Loading intent data from: {intents_path}")

    with open(intents_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    patterns = []
    labels = []
    intent_counts = {}

    for intent in data["intents"]:
        tag = intent["tag"]
        intent_patterns = intent.get("patterns", [])

        # Skip intents with no training patterns
        # (e.g., 'fallback' has no patterns by design)
        if not intent_patterns:
            print(f"  [SKIP] '{tag}' — no patterns (handled by "
                  f"confidence threshold)")
            continue

        intent_counts[tag] = len(intent_patterns)
        for pattern in intent_patterns:
            patterns.append(pattern)
            labels.append(tag)

    print(f"  ✔ Loaded {len(patterns)} patterns across "
          f"{len(intent_counts)} intents.")
    print(f"  Intent distribution:")
    for tag, count in sorted(intent_counts.items()):
        print(f"    {tag:<30} {count} patterns")

    return patterns, labels


# ============================================================
# Step 2: Preprocess Training Data
# ============================================================

def preprocess_patterns(patterns: list) -> list:
    """Apply the NLP preprocessing pipeline to all patterns.

    Calls nlp.preprocessor.preprocess() on each raw pattern
    string to produce cleaned, lemmatized text ready for
    TF-IDF vectorization.

    Parameters
    ----------
    patterns : list[str]
        Raw pattern strings from intents.json.

    Returns
    -------
    list[str]
        Preprocessed pattern strings.
    """
    print("\n[Step 2] Preprocessing training patterns...")

    preprocessed = [preprocess_classifier(p) for p in patterns]

    # Report any patterns that became empty after preprocessing
    empty_count = sum(1 for p in preprocessed if not p.strip())
    if empty_count > 0:
        print(f"  [WARNING] {empty_count} pattern(s) became empty "
              f"after preprocessing. Consider reviewing intents.json.")

    print(f"  ✔ Preprocessed {len(preprocessed)} patterns.")
    return preprocessed


# ============================================================
# Step 3: Fit TF-IDF Vectorizer and Transform
# ============================================================

def build_tfidf_features(preprocessed_patterns: list) -> tuple:
    """Fit a TF-IDF vectorizer and transform patterns to vectors.

    TF-IDF (Term Frequency – Inverse Document Frequency) converts
    text into numerical feature vectors. For each word:
    - TF (Term Frequency): how often it appears in this pattern.
    - IDF (Inverse Document Frequency): how rare it is across all
      patterns. Rare, distinctive words get higher IDF scores.

    The product TF × IDF gives the final feature weight, which
    is high for words that are important to a specific intent
    and low for words that appear everywhere (like common words
    that survived stopword removal).

    Hyperparameters chosen:
    - ngram_range=(1, 2): Include both unigrams (single words)
      and bigrams (pairs of adjacent words). Bigrams capture
      phrases like "weight loss" and "muscle gain" which have
      different meanings than their individual words.
    - max_features=5000: Limits vocabulary to 5000 most important
      features to prevent overfitting on a small dataset.
    - sublinear_tf=True: Apply log normalization to term frequency,
      which dampens the effect of very frequent terms.

    Parameters
    ----------
    preprocessed_patterns : list[str]
        Preprocessed text patterns.

    Returns
    -------
    tuple[TfidfVectorizer, sparse matrix]
        Fitted vectorizer and the transformed feature matrix.
    """
    print("\n[Step 3] Building TF-IDF feature vectors...")

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),       # Unigrams and bigrams
        max_features=5000,        # Cap vocabulary size
        sublinear_tf=True,        # Log-scale TF normalization
        strip_accents="unicode",  # Handle accented characters
    )

    X = vectorizer.fit_transform(preprocessed_patterns)
    vocab_size = len(vectorizer.vocabulary_)

    print(f"  ✔ Vocabulary size: {vocab_size} unique n-grams.")
    print(f"  ✔ Feature matrix shape: {X.shape} "
          f"(patterns × features).")

    return vectorizer, X


# ============================================================
# Step 4: Train Logistic Regression
# ============================================================

def train_classifier(X, labels: list) -> tuple:
    """Train a Logistic Regression classifier on the features.

    Splits data into training (80%) and test (20%) sets,
    trains the classifier on the training split, and returns
    both the trained model and the test split for evaluation.

    Logistic Regression Hyperparameters:
    - C=10: Inverse regularisation strength. Higher C = less
      regularisation, allowing the model to fit the training
      data more closely. Appropriate for a small, clean dataset.
    - max_iter=1000: Maximum iterations for the optimiser.
      Increased from default (100) to ensure convergence.
    - solver='lbfgs': Limited-memory BFGS optimisation algorithm,
      the recommended solver for multi-class LR in scikit-learn.
    - multi_class='auto': Automatically uses 'multinomial'
      for multi-class problems, which is more principled than
      the 'one-vs-rest' approach.
    - random_state=42: Ensures reproducible train-test splits.

    Parameters
    ----------
    X : sparse matrix
        TF-IDF feature matrix of shape (n_samples, n_features).
    labels : list[str]
        Intent labels corresponding to each row of X.

    Returns
    -------
    tuple[LogisticRegression, arrays]
        (trained_model, X_test, y_test) for evaluation.
    """
    print("\n[Step 4] Training Logistic Regression classifier...")

    # Split into training (80%) and test (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels,
        test_size=0.15,
        random_state=42,
        stratify=labels if _can_stratify(labels) else None
    )

    print(f"  Training samples : {X_train.shape[0]}")
    print(f"  Test samples     : {X_test.shape[0]}")

    # Train the Logistic Regression model
    model = LogisticRegression(
        C=1.0,
        max_iter=1000,
        solver="lbfgs",
        random_state=42,
    )
    model.fit(X_train, y_train)

    print(f"  ✔ Model trained successfully.")
    return model, X_test, y_test


def _can_stratify(labels: list) -> bool:
    """Check if stratified split is possible.

    Stratification requires each class to appear at least twice.
    Returns False if any class has fewer than 2 samples.
    """
    from collections import Counter
    counts = Counter(labels)
    return all(c >= 2 for c in counts.values())


# ============================================================
# Step 5: Evaluate Model Performance
# ============================================================

def evaluate_model(model, X_test, y_test) -> dict:
    """Evaluate classifier performance on the test split.

    Computes and prints:
    - Overall accuracy (percentage of correct predictions).
    - Per-class precision, recall, and F1-score.

    Precision = TP / (TP + FP)  — How accurate positive predictions are.
    Recall    = TP / (TP + FN)  — How many actual positives were found.
    F1-score  = 2 × (P × R) / (P + R) — Harmonic mean of P and R.

    Parameters
    ----------
    model : LogisticRegression
        The trained classifier.
    X_test : sparse matrix
        TF-IDF feature vectors for the test set.
    y_test : list[str]
        True intent labels for the test set.

    Returns
    -------
    dict
        Dictionary with 'accuracy' key and value.
    """
    print("\n[Step 5] Evaluating model performance...")

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n  {'='*50}")
    print(f"  ACCURACY : {accuracy * 100:.2f}%")
    print(f"  {'='*50}")
    print(f"\n  CLASSIFICATION REPORT:")
    print("  " + "-" * 60)
    report = classification_report(y_test, y_pred, zero_division=0)
    # Indent each line for cleaner console output
    for line in report.split("\n"):
        print(f"  {line}")

    return {"accuracy": accuracy}


# ============================================================
# Step 6: Save Trained Artefacts
# ============================================================

def save_artefacts(vectorizer, model) -> None:
    """Save the fitted vectorizer and trained model to disk.

    Uses joblib for serialisation, which is more efficient
    than Python's built-in pickle for objects containing
    large numpy arrays (such as the TF-IDF weight matrix).

    Parameters
    ----------
    vectorizer : TfidfVectorizer
        The fitted TF-IDF vectorizer to save.
    model : LogisticRegression
        The trained Logistic Regression model to save.
    """
    print("\n[Step 6] Saving trained artefacts...")

    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(model, MODEL_PATH)

    print(f"  ✔ Vectorizer saved → {VECTORIZER_PATH}")
    print(f"  ✔ Classifier saved → {MODEL_PATH}")


# ============================================================
# Main Training Orchestrator
# ============================================================

def train() -> None:
    """Run the full training pipeline end-to-end.

    Orchestrates all training steps in sequence:
    Load → Preprocess → Vectorize → Train → Evaluate → Save.
    """
    print("\n" + "=" * 60)
    print("  HealthFit AI Chatbot — Model Training")
    print("=" * 60)

    # Step 1: Load data
    patterns, labels = load_intent_data(INTENTS_PATH)

    # Step 2: Preprocess
    preprocessed = preprocess_patterns(patterns)

    # Step 3: TF-IDF vectorization
    vectorizer, X = build_tfidf_features(preprocessed)

    # Step 4: Train classifier
    model, X_test, y_test = train_classifier(X, labels)

    # Step 5: Evaluate
    evaluate_model(model, X_test, y_test)

    # Step 6: Save
    save_artefacts(vectorizer, model)

    print("\n" + "=" * 60)
    print("  Training complete. Model is ready for use.")
    print("=" * 60 + "\n")


# ============================================================
# Conditional Re-training
# ============================================================

def train_if_model_missing() -> None:
    """Trigger training only if model files do not exist.

    Called at application startup via nlp_service.py. Ensures
    the model is always available without requiring a manual
    training step from the user.
    """
    if (not os.path.exists(VECTORIZER_PATH)
            or not os.path.exists(MODEL_PATH)):
        print("[INFO] Model files not found. Starting training...")
        train()
    else:
        print("[INFO] Model files found. Skipping training.")


# ============================================================
# Script Entry Point
# ============================================================

if __name__ == "__main__":
    train()
