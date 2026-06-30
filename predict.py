"""
HealthFit AI Chatbot — Prediction Module

Provides a standalone interface for testing the trained
NLP pipeline from the command line. Loads the saved model
and vectorizer, processes a user input string, and returns
the predicted intent, confidence score, and bot response.

This module is useful for:
- Quickly testing the model after training.
- Debugging intent classification without running Flask.
- Demonstrating the NLP pipeline during the MCA viva.

Usage
-----
    # Interactive mode (prompts for input)
    python predict.py

    # Single prediction
    python predict.py "how many calories should i eat"

Functions
---------
load_pipeline(config)
    Load vectorizer, model, and response map from disk.
predict(user_input, vectorizer, model, response_map, threshold)
    Run the full pipeline on a single user input string.
interactive_mode(vectorizer, model, response_map, threshold)
    Run a REPL loop for testing predictions interactively.
"""

import os
import sys

# Ensure project root is on the path for imports
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import BaseConfig, DevelopmentConfig
from nlp.preprocessor import preprocess
from nlp.classifier import load_model, predict_intent
from nlp.response_generator import load_responses, get_response
from train_model import train_if_model_missing


# ============================================================
# Pipeline Loader
# ============================================================

def load_pipeline(config=DevelopmentConfig) -> tuple:
    """Load the trained model, vectorizer, and response map.

    Ensures model files exist (triggers training if not),
    then loads all three components needed for prediction.

    Parameters
    ----------
    config : Config class, optional
        Configuration class providing paths. Default is
        DevelopmentConfig.

    Returns
    -------
    tuple[TfidfVectorizer, LogisticRegression, dict]
        (vectorizer, model, response_map)
    """
    # Auto-train if model files are missing
    train_if_model_missing()

    # Load the trained artefacts
    vectorizer, model = load_model(
        vectorizer_path=config.VECTORIZER_PATH,
        model_path=config.CLASSIFIER_PATH
    )

    # Load the response map from intents.json
    response_map = load_responses(config.INTENTS_PATH)

    return vectorizer, model, response_map


# ============================================================
# Single Prediction
# ============================================================

def predict(user_input: str, vectorizer, model,
            response_map: dict,
            threshold: float = 0.60) -> dict:
    """Run the full NLP pipeline on a single user input.

    Steps:
    1. Preprocess the raw input text.
    2. Predict the intent with confidence score.
    3. Retrieve an appropriate response from the knowledge base.
    4. Return all four values as a result dictionary.

    Parameters
    ----------
    user_input : str
        The raw text typed by the user.
    vectorizer : TfidfVectorizer
        The fitted TF-IDF vectorizer.
    model : LogisticRegression
        The trained Logistic Regression classifier.
    response_map : dict
        The intent → [responses] mapping.
    threshold : float, optional
        Minimum confidence to accept the prediction.
        Default is 0.60.

    Returns
    -------
    dict
        {
            "user_input":       str,   # original input
            "cleaned_input":    str,   # after preprocessing
            "intent":           str,   # predicted intent tag
            "confidence":       float, # classifier confidence
            "response":         str    # selected response text
        }
    """
    # Step 1: Preprocess the raw input
    cleaned = preprocess(user_input)

    # Step 2: Classify intent and get confidence score
    intent, confidence = predict_intent(
        text=cleaned,
        vectorizer=vectorizer,
        model=model,
        threshold=threshold
    )

    # Step 3: Retrieve a response from the response map
    response = get_response(intent, response_map)

    return {
        "user_input": user_input,
        "cleaned_input": cleaned,
        "intent": intent,
        "confidence": confidence,
        "response": response,
    }


# ============================================================
# Interactive Mode
# ============================================================

def interactive_mode(vectorizer, model, response_map: dict,
                     threshold: float = 0.60) -> None:
    """Run a REPL loop for interactive intent prediction.

    Continuously prompts the user for input and prints the
    predicted intent, confidence score, and bot response.
    Type 'quit', 'exit', or 'q' to stop.

    Parameters
    ----------
    vectorizer, model, response_map, threshold
        Same as predict() — passed through to it.
    """
    print("\n" + "=" * 60)
    print("  HealthFit AI — Interactive Prediction Test")
    print("  Type your message to test intent classification.")
    print("  Type 'quit' to exit.")
    print("=" * 60 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nSession ended. Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Session ended. Stay healthy!")
            break

        result = predict(
            user_input=user_input,
            vectorizer=vectorizer,
            model=model,
            response_map=response_map,
            threshold=threshold
        )

        print(f"\n  [Cleaned Input] : {result['cleaned_input']}")
        print(f"  [Intent]        : {result['intent']}")
        print(f"  [Confidence]    : {result['confidence']:.4f} "
              f"({result['confidence'] * 100:.1f}%)")
        print(f"\nHealthFit AI: {result['response']}\n")
        print("-" * 60)


# ============================================================
# Script Entry Point
# ============================================================

if __name__ == "__main__":
    # Load the pipeline (auto-trains if model missing)
    vectorizer, model, response_map = load_pipeline()
    threshold = DevelopmentConfig.CONFIDENCE_THRESHOLD

    if len(sys.argv) > 1:
        # Single-query mode: predict for the command-line argument
        user_input = " ".join(sys.argv[1:])
        result = predict(user_input, vectorizer, model,
                         response_map, threshold)

        print("\n" + "=" * 60)
        print(f"  Input     : {result['user_input']}")
        print(f"  Cleaned   : {result['cleaned_input']}")
        print(f"  Intent    : {result['intent']}")
        print(f"  Confidence: {result['confidence']:.4f} "
              f"({result['confidence'] * 100:.1f}%)")
        print(f"\n  Response  : {result['response']}")
        print("=" * 60 + "\n")
    else:
        # Interactive REPL mode
        interactive_mode(vectorizer, model, response_map, threshold)
