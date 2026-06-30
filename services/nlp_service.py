"""
HealthFit AI Chatbot — NLP Service Layer

This module is the bridge between the chat controller and
the NLP engine. It initialises the full pipeline on startup
and exposes a single analyse_message() function to the rest
of the application.

Architecture Position
---------------------
    Chat Controller
        → nlp_service.analyse_message()
            → nlp.preprocessor.preprocess()
            → nlp.classifier.predict_intent()
            → nlp.response_generator.get_response()
        ← (intent, confidence, response)

Initialisation Strategy
-----------------------
Model components are loaded once at module import time and
stored in module-level variables. This ensures:
- No repeated disk I/O on every request.
- Consistent prediction results across all requests.
- Graceful startup error reporting if model files are missing.

The module calls train_if_model_missing() on first import,
which triggers training if the model .pkl files do not exist.
This means the application always works out-of-the-box, even
if train_model.py has never been run manually.

Functions
---------
analyse_message(message, confidence_threshold)
    Full NLP pipeline: preprocess → classify → respond.
_load_pipeline()
    Load the vectorizer, model, and response map from disk.
"""

import os
import sys
import logging
import re

# Ensure project root is on path for module imports
_PROJECT_ROOT = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)
))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from config import BaseConfig
from nlp.preprocessor import preprocess_classifier, preprocess_keywords
from nlp.classifier import load_model, predict_intent
from nlp.response_generator import load_responses, get_response
from nlp.entity_extractor import extract_entities
from train_model import train_if_model_missing

logger = logging.getLogger(__name__)

# ============================================================
# Module-level Pipeline Initialisation
# ============================================================
# These variables are populated by _load_pipeline() which is
# called once at module import time. They are module-level
# (not inside a function) so they are shared across all
# requests without re-loading from disk every time.

_vectorizer = None
_model = None
_response_map = None
_pipeline_ready = False


def _load_pipeline() -> None:
    """Initialise all NLP components from disk.

    Triggered once at module import. Auto-trains the model
    if the .pkl files are not yet present on disk.

    Sets the module-level variables:
    - _vectorizer : fitted TF-IDF vectorizer
    - _model      : trained Logistic Regression model
    - _response_map: dict mapping intent tags to response lists
    - _pipeline_ready: True if loading succeeded, False otherwise
    """
    global _vectorizer, _model, _response_map, _pipeline_ready

    try:
        # Auto-train if model files are missing
        train_if_model_missing()

        # Load vectorizer and classifier from disk
        _vectorizer, _model = load_model(
            vectorizer_path=BaseConfig.VECTORIZER_PATH,
            model_path=BaseConfig.CLASSIFIER_PATH
        )

        # Load the response map from intents.json
        _response_map = load_responses(BaseConfig.INTENTS_PATH)

        _pipeline_ready = True
        logger.info("NLP pipeline loaded successfully.")

    except (FileNotFoundError, ValueError, Exception) as exc:
        logger.error(
            "Failed to load NLP pipeline: %s. "
            "The chatbot will return error responses until "
            "the issue is resolved. Run train_model.py.",
            str(exc)
        )
        _pipeline_ready = False


# Load the pipeline immediately when this module is imported
_load_pipeline()


# ============================================================
# Public API
# ============================================================

def analyse_message(message: str,
                    confidence_threshold: float = 0.60,
                    context_history: list = None,
                    session_id: str = None,
                    db_path: str = None) -> tuple:
    """Process a user message through the complete hybrid, context-aware NLP pipeline.

    Parameters
    ----------
    message : str
        The raw text typed by the user.
    confidence_threshold : float, optional
        Minimum probability to accept the classifier's prediction.
        Default is 0.60.
    context_history : list, optional
        A list of recent user message strings representing the conversation history.
    session_id : str, optional
        The active session identifier.
    db_path : str, optional
        The path to the SQLite database.

    tuple[str, float, str, dict]
        (intent_label, confidence_score, response_text, extracted_entities)
    """
    # Guard: if pipeline failed to load, return a safe error reply
    if not _pipeline_ready:
        return (
            "error",
            0.0,
            "I am currently unable to process your request "
            "because the NLP model is not loaded. Please run "
            "'python train_model.py' to train the model and "
            "restart the server.",
            {}
        )

    # Step 0: Check for follow-up intent detection (Requirement 4)
    is_follow_up = False
    intent = None
    confidence = 0.0
    
    follow_up_phrases = {
        "explain it", "tell me more", "elaborate", "continue", "why", "how does that work",
        "how", "explain", "what next", "is that safe", "give me another option"
    }
    clean_msg = message.lower().strip().rstrip("?.!")
    
    if clean_msg in follow_up_phrases and context_history:
        # Walk backwards to find the last valid intent
        for item in reversed(context_history):
            prev_intent = item.get("detected_intent")
            if prev_intent and prev_intent not in ("fallback", "error"):
                # Handle multi-intent split if the previous intent was combined
                if "+" in prev_intent:
                    intent = prev_intent.split("+")
                else:
                    intent = prev_intent
                confidence = 1.0
                is_follow_up = True
                break

    # Step 1: Text Preprocessing for Classification (Requirement 2)
    cleaned_text = preprocess_classifier(message)

    # Step 2: Entity Extraction (Age, Weight, Height, Food, Exercises, Goals)
    entities = extract_entities(message)

    # Fetch stored profile data if session_id and db_path are provided
    profile = {}
    reused_attributes = []
    if session_id and db_path:
        from utils.db_manager import get_profile, save_profile
        try:
            profile = get_profile(db_path, session_id)
            
            # Save any newly extracted profile parameters to session profile
            profile_updates = {
                "weight": entities.get("weight"),
                "height": entities.get("height"),
                "age": entities.get("age"),
                "gender": entities.get("gender"),
                "goal": entities.get("fitness_goals")[0] if entities.get("fitness_goals") else None,
                "activity_level": entities.get("activity_level"),
                "water_intake": entities.get("water_intake")
            }
            
            if any(val is not None for val in profile_updates.values()):
                save_profile(db_path, session_id, profile_updates)
                # Refresh profile after save to ensure we have the absolute latest merged state
                profile = get_profile(db_path, session_id)
                
            # Merge previously provided metrics into entities if they are missing in current message
            if not entities.get("weight") and profile.get("weight"):
                entities["weight"] = profile["weight"]
                reused_attributes.append(f"weight of {profile['weight']}")
            if not entities.get("height") and profile.get("height"):
                entities["height"] = profile["height"]
                reused_attributes.append(f"height of {profile['height']}")
            if not entities.get("age") and profile.get("age") is not None:
                entities["age"] = profile["age"]
                reused_attributes.append(f"age of {profile['age']}")
            if not entities.get("gender") and profile.get("gender"):
                entities["gender"] = profile["gender"]
                reused_attributes.append(f"gender ({profile['gender']})")
            if not entities.get("fitness_goals") and profile.get("goal"):
                entities["fitness_goals"] = [profile["goal"]]
                reused_attributes.append(f"goal of {profile['goal'].replace('_', ' ')}")
            if not entities.get("activity_level") and profile.get("activity_level"):
                entities["activity_level"] = profile["activity_level"]
                reused_attributes.append(f"activity level of {profile['activity_level']}")
            if not entities.get("water_intake") and profile.get("water_intake"):
                entities["water_intake"] = profile["water_intake"]
                reused_attributes.append(f"water intake of {profile['water_intake']}")
                
        except Exception as e:
            logger.error(f"Error handling session profile in analyse_message: {e}")

    if not is_follow_up:
        # Step 3: Classify Intent on the Current Message Alone First (Requirement 3 & 5)
        # We only pull in history context lazy-style if the current message on its own falls back.
        intent, confidence = predict_intent(
            text=cleaned_text,
            vectorizer=_vectorizer,
            model=_model,
            threshold=confidence_threshold,
            raw_text=message
        )

        # Step 4: Vague Query Context Resolution (Requirement 5 & 8)
        # If the current query resolved to fallback AND we have a context history,
        # check if the input is short/vague (excluding social greetings/queries)
        # and try merging with past conversation history.
        if intent == "fallback" and context_history:
            social_indicators = {
                "how are you", "who are you", "what are you", "what is your name",
                "whats up", "what's up", "hello", "hi", "hey", "good morning",
                "good afternoon", "good evening", "how's it going", "how is it going",
                "thank you", "thanks", "how you doing", "how are things"
            }
            vague_indicators = {
                "not on track", "help me", "suggest", "explain", "better", "improve",
                "do that", "how to", "how do i", "what is that", "more", "tell me",
                "not right", "explain more", "what about", "is there any"
            }
            
            message_lower = message.lower()
            is_social = any(si in message_lower for si in social_indicators)
            
            is_vague = False
            if not is_social:
                has_vague_indicator = any(vi in message_lower for vi in vague_indicators)
                cleaned_words = cleaned_text.split()
                is_short = 0 < len(cleaned_words) <= 4
                is_vague = has_vague_indicator or is_short
            
            if is_vague:
                cleaned_history = []
                raw_history = []
                for item in context_history[-3:]:  # limit to last 3 exchanges
                    past_msg = item.get("user_message", "")
                    if past_msg and past_msg.strip():
                        clean_h = preprocess_classifier(past_msg)
                        if clean_h:
                            cleaned_history.append(clean_h)
                            raw_history.append(past_msg)
                if cleaned_history:
                    # Prepend context to help identify the active topic
                    classification_text = " ".join(cleaned_history) + " " + cleaned_text
                    raw_text_with_context = " ".join(raw_history) + " " + message
                    
                    # Re-classify with merged context
                    intent, confidence = predict_intent(
                        text=classification_text,
                        vectorizer=_vectorizer,
                        model=_model,
                        threshold=confidence_threshold,
                        raw_text=raw_text_with_context
                    )

    # Guard: If preprocessed cleaned text is empty and we have no valid intent, route to fallback response
    if not cleaned_text.strip() and intent == "fallback":
        response = get_response("fallback", _response_map)
        intent_str = "fallback"
    else:
        # Step 5: Dynamic Template Rendering & Multi-Intent Response Combination (Requirements 4 & 6)
        if isinstance(intent, list):
            # Multi-intent detected: retrieve and combine responses
            responses_list = []
            for tag in intent:
                raw_resp = get_response(tag, _response_map)
                formatted_resp = format_dynamic_response(tag, raw_resp, entities)
                responses_list.append(formatted_resp)
            
            response = (
                "I noticed you are asking about multiple topics! "
                "Here is some personalized advice on both:\n\n" + 
                "\n\n---\n\n".join(responses_list)
            )
            intent_str = "+".join(intent)
        else:
            # Single intent: retrieve and format dynamically
            raw_resp = get_response(intent, _response_map)
            response = format_dynamic_response(intent, raw_resp, entities)
            intent_str = intent

        # Prepend composed entity intro if any entities were detected (Requirement 4)
        if intent_str not in ("fallback", "error"):
            composed_intro = compose_natural_entity_response(entities)
            if composed_intro:
                response = f"{composed_intro}\n\n{response}"

        # Prepend reused attributes reminder to personalize the response (Requirement 5)
        if reused_attributes and intent_str not in ("fallback", "error"):
            if len(reused_attributes) == 1:
                attr_str = reused_attributes[0]
            else:
                attr_str = ", ".join(reused_attributes[:-1]) + ", and " + reused_attributes[-1]
            reused_intro = f"Based on your previously provided {attr_str}:"
            response = f"{reused_intro}\n\n{response}"

    # Step 6: Log detailed NLP execution metadata for debugging and viva demonstrations (Requirement 7)
    logger.info(
        "\n" + "=" * 50 + "\n"
        "  HealthFit AI Hybrid NLP Engine Pipeline Trace\n"
        "  " + "-" * 46 + "\n"
        f"  • Raw Input            : '{message}'\n"
        f"  • Preprocessed Text    : '{cleaned_text}'\n"
        f"  • Predicted Intent(s)  : '{intent_str}'\n"
        f"  • Confidence Score     : {confidence:.4f}\n"
        f"  • Extracted Entities   : {entities}\n"
        f"  • Selected Response    : '{response[:80].strip()}...'\n" +
        "=" * 50
    )

    return intent_str, confidence, response, entities


# ============================================================
# Dynamic Formatting & Calculator Helpers
# ============================================================

def parse_height_cm(height_str: str) -> float:
    """Parse height string and return height in centimeters."""
    if not height_str:
        return None
    # 1. Check for cm: e.g. "175 cm", "175cm"
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:cm|cms|centimeters?)', height_str, re.IGNORECASE)
    if match:
        return float(match.group(1))
    
    # 2. Check for m: e.g. "1.75 m"
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:meters?|m)\b', height_str, re.IGNORECASE)
    if match:
        val = float(match.group(1))
        if val < 3.0:
            return val * 100
        return val
        
    # 3. Check for feet/inches: e.g. "5ft 10in", "5'10"
    match = re.search(r'(\d+)\s*(?:feet|ft|foot|\'|’)\s*(?:(\d+)\s*(?:inches?|in|ins|\"|”|))?', height_str, re.IGNORECASE)
    if match:
        feet = float(match.group(1))
        inches = float(match.group(2)) if match.group(2) else 0.0
        return (feet * 12 + inches) * 2.54
        
    # 4. Fallback: try to grab first number
    match = re.search(r'(\d+(?:\.\d+)?)', height_str)
    if match:
        val = float(match.group(1))
        if val < 3.0:
            return val * 100
        return val
    return None


def parse_weight_kg(weight_str: str) -> float:
    """Parse weight string and return weight in kilograms."""
    if not weight_str:
        return None
    # 1. Check for kg: e.g. "70 kg"
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:kg|kgs|kilograms?)', weight_str, re.IGNORECASE)
    if match:
        return float(match.group(1))
        
    # 2. Check for lbs: e.g. "154 lbs"
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:lbs?|pounds?)', weight_str, re.IGNORECASE)
    if match:
        return float(match.group(1)) * 0.45359237
        
    # 3. Fallback: try to grab first number
    match = re.search(r'(\d+(?:\.\d+)?)', weight_str)
    if match:
        val = float(match.group(1))
        if val > 120:
            return val * 0.45359237
        return val
    return None


def format_dynamic_response(intent: str, response_template: str, entities: dict) -> str:
    """Replaces placeholders in response templates with parsed entity details and BMR/BMI calculations."""
    if not response_template:
        return ""

    height_str = entities.get("height")
    weight_str = entities.get("weight")
    age = entities.get("age")
    gender = entities.get("gender")
    
    height_cm = parse_height_cm(height_str)
    weight_kg = parse_weight_kg(weight_str)

    # 1. Format BMI placeholder
    if "{bmi_calc}" in response_template:
        if height_cm and weight_kg:
            height_m = height_cm / 100.0
            bmi = round(weight_kg / (height_m * height_m), 2)
            
            if bmi < 18.5:
                cat = "Underweight"
                adv = "Focus on healthy caloric surpluses, nutrient-dense carbs, and strength training. Consult a dietitian if needed."
            elif 18.5 <= bmi <= 24.9:
                cat = "Normal (Healthy Weight)"
                adv = "Great job! Maintain your current balanced lifestyle, focusing on clean eating and consistent training."
            elif 25.0 <= bmi <= 29.9:
                cat = "Overweight"
                adv = "Incorporate regular cardio, full-body resistance sessions, and maintain a slight daily calorie deficit of 300-500 kcal."
            else:
                cat = "Obese"
                adv = "Create a structured, physician-approved weight management program focusing on steady, consistent progress."
            
            calc_text = f"\n\n👉 **Your Personal BMI Result:**\n• **Height:** {height_str}\n• **Weight:** {weight_str}\n• **BMI Score:** **{bmi}**\n• **Category:** **{cat}**\n• **Direct Advice:** {adv}"
        else:
            calc_text = "\n\nTo calculate your BMI right now, please specify your weight (e.g., '72 kg') and height (e.g., '180 cm') in your query."
        response_template = response_template.replace("{bmi_calc}", calc_text)

    # 2. Format Calorie Advice placeholder
    if "{calorie_advice}" in response_template:
        if height_cm and weight_kg:
            user_age = age or 25
            user_gender = gender or "male"
            
            # BMR Estimation (Mifflin-St Jeor)
            if user_gender == "female":
                bmr = 10 * weight_kg + 6.25 * height_cm - 5 * user_age - 161
            else:
                bmr = 10 * weight_kg + 6.25 * height_cm - 5 * user_age + 5
            
            bmr = int(bmr)
            tdee = int(bmr * 1.55) # Assuming moderate activity multiplier
            deficit = tdee - 400
            surplus = tdee + 300
            
            cal_text = (
                f"\n\n👉 **Estimated Daily Calorie Breakdown:**\n"
                f"• **Basal Metabolic Rate (BMR):** **{bmr} kcal/day** (resting requirements)\n"
                f"• **Maintenance Calories (TDEE):** **{tdee} kcal/day** (includes activity)\n"
                f"• **Calorie Deficit Goal (Weight Loss):** **{deficit} kcal/day**\n"
                f"• **Calorie Surplus Goal (Muscle Gain):** **{surplus} kcal/day**"
            )
        else:
            cal_text = "\n\nIf you provide your weight, height, age, and gender, I can estimate your daily Basal Metabolic Rate (BMR) and recommended calories!"
        response_template = response_template.replace("{calorie_advice}", cal_text)

    # 3. Format Hydration Advice placeholder
    if "{hydration_advice}" in response_template:
        if weight_kg:
            water_ml = int(weight_kg * 35)
            water_liters = round(water_ml / 1000.0, 2)
            cups = round(water_ml / 250.0, 1)
            hydro_text = f"\n\n👉 **Recommended Hydration Goal:**\n• **Target:** **{water_liters} Liters/day** (about **{cups}** cups) based on your weight of {weight_str}."
        else:
            hydro_text = "\n\n(Tip: Active adults generally require 3 to 4 liters of water daily to prevent dehydration. Let me know your weight for a personalized target.)"
        response_template = response_template.replace("{hydration_advice}", hydro_text)

    # 4. Format Sleep Advice placeholder
    if "{sleep_advice}" in response_template:
        if age:
            if age < 18:
                hours = "8–10 hours"
            elif 18 <= age <= 64:
                hours = "7–9 hours"
            else:
                hours = "7–8 hours"
            sleep_text = f"\n\n👉 **Sleep Suggestion:**\n• Based on your age of {age}, aim for **{hours}** of sleep per night to maximize recovery and performance."
        else:
            sleep_text = "\n\n(Note: Healthy adults typically require 7 to 9 hours of uninterrupted sleep per night for metabolic recovery.)"
        response_template = response_template.replace("{sleep_advice}", sleep_text)

    # 5. Format Exercise Advice placeholders
    for pl in ["{weight_loss_exercise_advice}", "{muscle_gain_exercise_advice}", "{cardio_advice}", "{squats_advice}", "{pushups_advice}"]:
        if pl in response_template:
            if entities.get("exercise_names"):
                exercises_mentioned = ", ".join(entities["exercise_names"])
                ex_text = f"\n\n👉 **Your Activity Highlight:**\n• Since you mentioned **{exercises_mentioned}**, make sure to keep proper form and progressive loading."
            else:
                ex_text = "\n\n(Tip: Focus on compound, multi-joint movements like squats, lunges, and pushups. Strive for 150 minutes of moderate activity weekly.)"
            response_template = response_template.replace(pl, ex_text)

    # 6. Format Diet/Nutrition Advice placeholders
    for pl in ["{keto_advice}", "{vegan_advice}", "{fat_loss_advice}", "{oats_advice}", "{chicken_advice}", "{salad_advice}", "{eggs_advice}", "{fish_advice}", "{whey_advice}"]:
        if pl in response_template:
            if entities.get("food_names"):
                foods_mentioned = ", ".join(entities["food_names"])
                diet_text = f"\n\n👉 **Your Food Highlight:**\n• You mentioned eating **{foods_mentioned}**, which is an excellent addition to support your daily macros."
            else:
                diet_text = ""
            response_template = response_template.replace(pl, diet_text)

    # Clean up any remaining unformatted placeholders (e.g. {obesity_advice}) to avoid exposing template tags
    response_template = re.sub(r'\{[a-zA-Z0-9_-]+\}', '', response_template)

    return response_template


def compose_natural_entity_response(entities: dict) -> str:
    """Compose a natural personalized introduction combining detected entities.
    
    This fulfills Phase 6.4 (Dynamic Response Templates) by identifying goals,
    exercises, and foods in the query and weaving them into conversational sentences.
    """
    if not entities:
        return ""
        
    goals = entities.get("fitness_goals", [])
    exercises = entities.get("exercise_names", [])
    foods = entities.get("food_names", [])
    
    if not (goals or exercises or foods):
        return ""
        
    parts = []
    
    # 1. Goal Sentence
    if goals:
        primary_goal = goals[0]
        if primary_goal == "weight_loss":
            parts.append("I see that your goal is weight loss.")
        elif primary_goal == "muscle_gain":
            parts.append("I see that your goal is muscle gain.")
        elif primary_goal == "endurance":
            parts.append("I see that your goal is improving endurance.")
        elif primary_goal == "maintenance":
            parts.append("I see that your goal is maintaining your fitness level.")
            
    # 2. Exercise Sentence
    if exercises:
        ex_formatted = [ex.capitalize() for ex in exercises]
        if len(ex_formatted) == 1:
            ex_str = ex_formatted[0]
            if ex_str.lower() in ["running", "jogging", "cycling", "swimming", "rowing", "cardio", "hiit"]:
                parts.append(f"{ex_str} is an excellent cardiovascular exercise.")
            elif ex_str.lower() in ["squat", "squats", "pushup", "pushups", "push-up", "push-ups", "pullup", "pullups", "bench press", "deadlift", "deadlifts"]:
                parts.append(f"{ex_str} is a highly effective strength-building movement.")
            else:
                parts.append(f"{ex_str} is an excellent exercise to support your fitness journey.")
        else:
            ex_str = ", ".join(ex_formatted[:-1]) + " and " + ex_formatted[-1]
            parts.append(f"Integrating {ex_str} into your routine is fantastic for your training.")

    # 3. Food Sentence
    if foods:
        food_formatted = [f.capitalize() for f in foods]
        if len(food_formatted) == 1:
            f_str = food_formatted[0]
            if f_str.lower() in ["chicken", "chicken breast", "turkey", "beef", "steak", "fish", "salmon", "tuna", "egg", "eggs", "egg white", "egg whites", "tofu", "paneer", "tempeh", "whey protein"]:
                parts.append(f"{f_str} is a great lean protein source.")
            elif f_str.lower() in ["apple", "banana", "orange", "grape", "berries", "strawberry", "blueberry", "fruit", "fruits", "broccoli", "spinach", "kale", "lettuce", "cucumber", "tomato", "vegetable", "veggies", "salad"]:
                parts.append(f"{f_str} is packed with essential micronutrients and fiber.")
            else:
                parts.append(f"{f_str} is a solid nutritional choice to fuel your body.")
        else:
            f_str = ", ".join(food_formatted[:-1]) + " and " + food_formatted[-1]
            parts.append(f"Consuming {f_str} is excellent for fueling your body and recovering efficiently.")

    # 4. Tailored advice sentence based on goal
    if goals:
        primary_goal = goals[0]
        if primary_goal == "weight_loss":
            parts.append("To maximize fat loss, combine regular exercise with a moderate calorie deficit.")
        elif primary_goal == "muscle_gain":
            parts.append("To maximize muscle hypertrophy, combine progressive resistance training with a small caloric surplus.")
        elif primary_goal == "endurance":
            parts.append("Focus on progressive aerobic training and optimal carbohydrate hydration to build stamina.")
        elif primary_goal == "maintenance":
            parts.append("Aim for balanced daily nutrition and consistent physical activity to sustain your health.")

    return " ".join(parts)



