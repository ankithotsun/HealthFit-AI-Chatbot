"""
HealthFit AI Chatbot — Intent Classifier

This module loads the trained TF-IDF + Logistic Regression
pipeline from disk and provides intent prediction with
confidence scores.

Architecture
------------
The classifier uses a two-stage pipeline:

1. TF-IDF Vectorizer (Term Frequency – Inverse Document Frequency)
   Converts preprocessed text into a numerical feature vector.
   Each word in the vocabulary gets a weight that reflects how
   important it is in this document relative to all documents.
   Words that appear in many documents (low IDF) are weighted
   lower; words that are distinctive to specific intents are
   weighted higher.

2. Logistic Regression Classifier
   A supervised learning algorithm that learns the relationship
   between TF-IDF feature vectors and intent labels. It models
   the probability of each class and returns both the predicted
   label and the probability score (confidence).

   Why Logistic Regression over alternatives?
   - Native probability output — unlike SVM, LR gives true
     probability scores which we use for the confidence threshold.
   - Highly interpretable — the learned weights show which words
     most influence each intent class (good for viva explanation).
   - Performs well on linearly separable text classification tasks.
   - Fast training and prediction.
   - Regularisation (C parameter) prevents overfitting on small
     datasets.

Model Persistence
-----------------
Trained artefacts are saved to disk using joblib:
- models_ml/tfidf_vectorizer.pkl  (fitted TF-IDF vectorizer)
- models_ml/trained_model.pkl     (fitted Logistic Regression)

At runtime, these are loaded once and cached in module-level
variables to avoid repeated disk reads.

Functions
---------
predict_intent(text, vectorizer, model, threshold)
    Predict the intent for a preprocessed text string.
load_model(vectorizer_path, model_path)
    Load both artefacts from disk and return them.
"""

import os
import re
import logging
import joblib

logger = logging.getLogger(__name__)

# Intent alias mapping for direct pre-classification matching
_INTENT_ALIASES = {
    # Weight Loss aliases
    "fat": "workout_weight_loss",
    "fat loss": "workout_weight_loss",
    "lose fat": "workout_weight_loss",
    "slim": "workout_weight_loss",
    "lean": "workout_weight_loss",
    "burn fat": "workout_weight_loss",
    
    # Muscle Gain aliases
    "bulk": "workout_muscle_gain",
    "bulk up": "workout_muscle_gain",
    "gain size": "workout_muscle_gain",
    "build muscles": "workout_muscle_gain",
    "be stronger": "workout_muscle_gain",
    
    # Workout aliases
    "gym": "workout_beginner",
    "exercise": "workout_beginner",
    "training": "workout_beginner",
    "lifting": "workout_beginner"
}


# ============================================================
# Model Loading
# ============================================================

def load_model(vectorizer_path: str, model_path: str) -> tuple:
    """Load the TF-IDF vectorizer and Logistic Regression model.

    Both artefacts are loaded from disk using joblib, which
    is the recommended serialisation method for scikit-learn
    objects (more efficient than pickle for large numpy arrays).

    Parameters
    ----------
    vectorizer_path : str
        Absolute path to the saved TF-IDF vectorizer (.pkl).
    model_path : str
        Absolute path to the saved Logistic Regression model (.pkl).

    Returns
    -------
    tuple[TfidfVectorizer, LogisticRegression]
        A 2-tuple of (fitted vectorizer, fitted classifier).

    Raises
    ------
    FileNotFoundError
        If either file does not exist at the specified path.
    """
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(
            f"Vectorizer not found at: {vectorizer_path}\n"
            "Please run train_model.py first to train and "
            "save the model."
        )

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Classifier not found at: {model_path}\n"
            "Please run train_model.py first to train and "
            "save the model."
        )

    vectorizer = joblib.load(vectorizer_path)
    model = joblib.load(model_path)

    return vectorizer, model


# ============================================================
# Intent Prediction (Hybrid & Multi-Intent)
# ============================================================

# Highly specific keywords for intent boosting (Hybrid NLP Classifier)
KEYWORD_BOOST_MAP = {
    "greeting": ["hello", "hi", "hey", "namaste", "greetings", "howdy", "how are you", "how's it going", "how have you been", "good morning", "good afternoon", "good evening", "helo", "hy", "goodevening", "goodmorning", "nice to meet you", "nice to meet u"],
    "goodbye": ["bye", "goodbye", "see you", "see you later", "take care", "farewell", "exit", "quit", "good night", "byebye", "tata"],
    "thanks": ["thank you", "thanks", "helpful", "perfect", "awesome", "appreciate", "thank u", "shukriya", "dhanyawad", "thankyou", "thx"],
    "help": ["help", "helper", "guide", "support", "madad"],
    "bot_identity": ["who are you", "your name", "about yourself", "what are you", "introduce yourself", "who made you", "developer info", "system designer", "who created you"],
    "bmi": ["bmi", "body mass index", "calculator", "height and weight", "bmiscore"],
    "calorie_estimation": ["calorie", "calories", "kcal", "burn calories", "daily calorie", "caloris"],
    "hydration": ["water", "hydrate", "hydration", "dehydrate", "drink water", "pina"],
    "sleep": ["sleep", "insomnia", "bedtime", "rest", "tired", "wake up", "sona"],
    "workout_beginner": ["beginner", "beginners", "start exercising", "newbie", "newbies", "gym beginner", "gym start", "start", "starting"],
    "workout_weight_loss": ["lose weight", "weight loss", "fat loss", "lose fat", "burn fat", "shed weight", "get lean", "hiit", "patla", "fatloss", "ghataye", "kam kare"],
    "workout_muscle_gain": ["gain muscle", "build muscle", "muscle gain", "bulk up", "grow muscle", "hypertrophy", "muscle building", "muscel", "bulkup"],
    "healthy_breakfast": ["breakfast", "morning meal", "nashte", "nashta"],
    "healthy_lunch": ["lunch", "midday meal", "khana"],
    "healthy_dinner": ["dinner", "night meal", "dinner diet"],
    "dietary_patterns": ["keto", "ketogenic", "vegan", "plant-based", "plant based", "vegetarian", "no meat", "intermittent fasting", "fasting window", "fasting"],
    "healthy_snacks": ["snack", "snacks", "fruit", "fruits", "vegetable", "vegetables", "veggies", "snacking", "snack options"],
    "protein_sources": ["protein", "protein sources", "whey", "protein powder", "protien", "protin"],
    "motivation": ["motivation", "motivated", "motivate", "consistent", "consistency", "feel lazy", "discipline", "mindset", "lazy"],
    "stress_management": ["stress", "anxiety", "cortisol", "relax", "meditate", "meditation"],
    "yoga_stretching": ["yoga", "asana", "stretch", "stretching", "flexibility", "mobility", "stretching exercise", "flexibilty"],
    "cardio_workout": ["cardio", "run", "running", "jog", "jogging", "cycling", "swim", "swimming", "stamina", "endurance"],
    "strength_training": ["strength", "weightlifting", "lifting", "deadlift", "bench press", "scapula", "upper body", "strength training"],
    "body_weight_exercises": ["pushup", "pushups", "push up", "push ups", "pushps", "pushps", "pullup", "pullups", "pull up", "pull ups", "plank", "planks", "plnk", "calisthenics", "bodyweight"],
    "leg_exercises": ["squat", "squats", "lunge", "lunges", "leg workout", "quads", "glutes", "hamstrings", "leg training"],
    "arm_exercises": ["bicep curl", "bicep curls", "arm curls", "tricep dips", "arms", "bicep", "biceps", "tricep", "triceps", "curl", "curls"],
    "abdominal_exercises": ["core", "abs", "ab routine", "six pack", "crunches", "situps"],
    "weight_issues": ["obese", "obesity", "overweight", "underweight", "skinny", "gain weight", "too thin", "mota"],
    "healthy_carb_sources": ["oats", "oatmeal", "banana", "bananas", "apple", "apples", "carbs"],
    "healthy_protein_foods": ["chicken breast", "chicken", "egg", "eggs", "fish", "salmon", "tuna"],
    "healthy_fat_sources": ["avocado", "avocados", "nuts", "almonds", "walnuts", "cashews"],
    "healthy_greens": ["salad", "salads", "broccoli", "spinach", "yogurt", "greek yogurt", "curd"],
    "emergency_disclaimer": ["chest pain", "heart attack", "shortness of breath", "emergency", "doctor", "hospital"]
}


def predict_intent(text: str, vectorizer,
                   model, threshold: float = 0.60,
                   raw_text: str = None) -> tuple:
    """Predict the intent of preprocessed user input.

    Uses a hybrid approach combining TF-IDF + Logistic Regression probability
    scores with keyword boosting, and supports multi-intent detection.

    Parameters
    ----------
    text : str
        Preprocessed text (output of nlp.preprocessor.preprocess).
    vectorizer : TfidfVectorizer
        The fitted TF-IDF vectorizer loaded from disk.
    model : LogisticRegression
        The fitted Logistic Regression classifier loaded from disk.
    threshold : float, optional
        Minimum confidence required to accept the prediction.
        If the highest class probability is below this value,
        the function returns the 'fallback' intent. Default 0.60.
    raw_text : str, optional
        The original raw query typed by the user, used for keyword boosting.

    Returns
    -------
    tuple[str or list, float]
        (intent_label_or_labels, confidence_score).
        If multiple intents are detected, intent_label_or_labels is a list.
    """
    # Guard against empty input
    if not text.strip():
        return "fallback", 0.0

    # Step 0: Check Alias Layer before classification
    from nlp.preprocessor import preprocess_keywords
    clean_kw_text = preprocess_keywords(raw_text) if raw_text else preprocess_keywords(text)
    for alias, target_intent in _INTENT_ALIASES.items():
        alias_clean = preprocess_keywords(alias)
        if clean_kw_text == alias_clean:
            logger.info(f"Alias matched: '{raw_text or text}' -> '{target_intent}'")
            return target_intent, 1.0

    # Step 1: Transform the preprocessed text into a TF-IDF feature vector
    feature_vector = vectorizer.transform([text])

    # Check if there is any word overlap with the vectorizer vocabulary
    # Out-of-scope/unrelated queries will have zero vocabulary overlap
    classifier_words = text.split()
    vocab = vectorizer.vocabulary_
    has_overlap = any(word in vocab for word in classifier_words)
    if not has_overlap:
        logger.info(f"Out-of-scope check: no vocabulary overlap for classifier words: {classifier_words}")
        return "fallback", 0.0

    # Step 2: Get class list and raw probability distribution from model
    classes = list(model.classes_)
    probabilities = list(model.predict_proba(feature_vector)[0])

    # Step 3: Apply Keyword Boosting (Hybrid Model)
    # Scan the text for specific fitness keywords and boost probabilities
    text_to_match = (raw_text or text).lower()
    boosted_probabilities = list(probabilities)
    for idx, class_label in enumerate(classes):
        if class_label in KEYWORD_BOOST_MAP:
            for kw in KEYWORD_BOOST_MAP[class_label]:
                # Require boundary matching or raw substring check for robustness
                if kw.lower() in text_to_match:
                    boosted_probabilities[idx] += 1.5
                    break  # Apply boost once per class

    # Step 4: Re-normalize probabilities so they sum to 1.0
    sum_probs = sum(boosted_probabilities)
    if sum_probs > 0:
        boosted_probabilities = [p / sum_probs for p in boosted_probabilities]

    # Step 5: Pair classes with their boosted probabilities and sort
    class_probs = list(zip(classes, boosted_probabilities))
    class_probs.sort(key=lambda x: x[1], reverse=True)

    primary_intent, primary_confidence = class_probs[0]

    # Step 6: Multi-Intent Detection
    # If a secondary intent has a boosted probability above 0.28, return both
    secondary_intents = [
        intent for intent, prob in class_probs[1:]
        if prob >= 0.38 and intent != "fallback"
    ]

    # Apply fallback logic if primary intent is low confidence
    if primary_confidence < threshold and not secondary_intents:
        # Check if any keyword matches before defaulting to fallback (Requirement 8)
        # If we have a keyword boost, we can accept a lower threshold (e.g. 0.40)
        has_boost = False
        if primary_intent in KEYWORD_BOOST_MAP:
            for kw in KEYWORD_BOOST_MAP[primary_intent]:
                if kw in text_to_match:
                    has_boost = True
                    break
        if not has_boost or primary_confidence < 0.35:
            return "fallback", round(primary_confidence, 4)

    if secondary_intents and primary_intent != "fallback":
        # Limit to top 2 intents to avoid cluttering
        selected_intents = [primary_intent] + secondary_intents[:1]
        return selected_intents, round(primary_confidence, 4)

    return primary_intent, round(primary_confidence, 4)

