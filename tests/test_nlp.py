"""
HealthFit AI Chatbot — NLP and Conversational Logic Integration Tests

This module implements unit and integration tests to verify the recent NLP improvements,
including:
1. Dual preprocessing pipelines: preprocess_classifier() and preprocess_keywords().
2. Correct intent classification of the expanded greetings dataset.
3. Follow-up intent detection and inheritance of conversational context.
"""

import sys
import os

# Put project root in system path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from nlp.preprocessor import preprocess_classifier, preprocess_keywords
from services.nlp_service import analyse_message


def test_dual_preprocessing_pipelines():
    """Verify that the preprocessing pipelines satisfy the split requirements."""
    test_phrase = "How are you? I am running and lifting weights!"
    
    # preprocess_classifier() must lowercase, remove punctuation, normalize whitespace,
    # and MUST NOT remove stopwords or lemmatize.
    classifier_processed = preprocess_classifier(test_phrase)
    assert "how" in classifier_processed
    assert "are" in classifier_processed
    assert "you" in classifier_processed
    assert "running" in classifier_processed  # Not lemmatized to "run"
    assert "weights" in classifier_processed  # Not lemmatized to "weight"
    assert "?" not in classifier_processed
    assert "!" not in classifier_processed
    
    # preprocess_keywords() must lowercase, remove punctuation, remove stopwords, and lemmatize.
    keywords_processed = preprocess_keywords(test_phrase)
    # Stopwords should be removed
    assert "how" not in keywords_processed
    assert "are" not in keywords_processed
    assert "you" not in keywords_processed
    # Words should be lemmatized (and potentially synonym-normalized by WordNet)
    # Note: 'running' -> 'run', 'lifting' -> 'lift', 'weights' -> 'weight' -> concept 'weight'
    assert "run" in keywords_processed or "running" not in keywords_processed
    assert "weight" in keywords_processed or "weights" not in keywords_processed


def test_greeting_dataset_expansion():
    """Verify that all newly added greetings classify correctly as 'greeting'."""
    greetings = [
        "how are you",
        "how's it going",
        "how have you been",
        "good morning",
        "good afternoon",
        "good evening",
        "nice to meet you"
    ]
    
    for phrase in greetings:
        intent_str, confidence, response, entities = analyse_message(phrase)
        assert intent_str == "greeting", f"Failed for phrase: {phrase} (got intent {intent_str})"
        assert confidence > 0.60, f"Confidence too low for phrase: {phrase} ({confidence})"
        assert len(response) > 0


def test_follow_up_intent_inheritance():
    """Verify that follow-up phrases correctly inherit the previous intent."""
    follow_ups = [
        "explain it",
        "tell me more",
        "elaborate",
        "continue",
        "why",
        "how does that work",
        "how",
        "explain",
        "what next",
        "is that safe",
        "give me another option"
    ]
    
    # Create a mock context history where the last detected intent was 'bmi'
    mock_history = [
        {
            "user_message": "What is my BMI?",
            "detected_intent": "bmi",
            "bot_response": "BMI evaluates weight relative to height."
        }
    ]
    
    for phrase in follow_ups:
        intent_str, confidence, response, entities = analyse_message(
            message=phrase,
            confidence_threshold=0.45,
            context_history=mock_history
        )
        assert intent_str == "bmi", f"Follow-up phrase '{phrase}' failed to inherit 'bmi' intent (got {intent_str})"
        assert confidence == 1.0, f"Follow-up confidence should be set to 1.0 (got {confidence})"
        # Make sure it generates a bmi-related response
        assert "BMI" in response or "weight" in response or "height" in response

    # Also test multi-intent inheritance (e.g. 'workout_muscle_gain+strength_training')
    mock_multi_history = [
        {
            "user_message": "Suggest exercises to gain muscle",
            "detected_intent": "workout_muscle_gain+strength_training",
            "bot_response": "Advice on both muscle gain and strength training."
        }
    ]
    
    for phrase in ["explain it", "elaborate"]:
        intent_str, confidence, response, entities = analyse_message(
            message=phrase,
            confidence_threshold=0.45,
            context_history=mock_multi_history
        )
        assert intent_str == "workout_muscle_gain+strength_training"
        assert confidence == 1.0
        assert "multiple topics" in response


def test_intent_aliases():
    """Verify that shorthand terms correctly match intent aliases before classification."""
    aliases_tests = {
        "fat": "workout_weight_loss",
        "fat loss": "workout_weight_loss",
        "bulk up": "workout_muscle_gain",
        "gym": "workout_beginner",
        "exercise": "workout_beginner"
    }
    for query, expected in aliases_tests.items():
        intent_str, confidence, _, _ = analyse_message(query)
        assert intent_str == expected, f"Query '{query}' failed alias mapping: expected {expected}, got {intent_str}"
        assert confidence == 1.0, f"Alias match confidence should be 1.0, got {confidence}"


def test_session_memory():
    """Verify that physical metrics and goals are persisted and reused across requests."""
    from utils.db_manager import init_db
    import tempfile
    
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
        
    try:
        init_db(db_path)
        session_id = "test_session_123"
        
        # 1. Provide weight in first message
        intent_str, confidence, response, entities = analyse_message(
            message="I weigh 80 kg.",
            session_id=session_id,
            db_path=db_path
        )
        assert entities.get("weight") == "80 kg"
        
        # 2. Ask another question later (which doesn't contain weight)
        intent_str, confidence, response, entities = analyse_message(
            message="How much protein should I eat?",
            session_id=session_id,
            db_path=db_path
        )
        assert entities.get("weight") == "80 kg"
        assert "80 kg" in response
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
