"""
HealthFit AI Chatbot — Entity Extraction Module

This module extracts physical metrics (height, weight, age, gender), health-related
entities (food names, exercise names, quantities), and fitness goals from user messages
using regular expressions and keyword matching.

Features:
- Extracts height (cm, meters, feet/inches).
- Extracts weight (kg, lbs).
- Extracts age (years, ages, numbers associated with age).
- Extracts gender (male, female, non-binary).
- Extracts food items based on a curated glossary.
- Extracts exercises based on a curated glossary.
- Extracts quantities (servings, weights, repetitions, durations).
- Extracts fitness goals (weight loss, muscle gain, endurance, maintenance).
"""

import re
from typing import Dict, List, Any

# =====================================================================
# Regular Expression Patterns (Case-Insensitive)
# =====================================================================

# Matches height patterns: e.g., "175 cm", "175cm", "1.75 m", "1.8 meters", "5ft 10in", "5'10\""
HEIGHT_PATTERNS = [
    re.compile(r'\b\d+(?:\.\d+)?\s*(?:cm|cms|centimeters?|meters?|m)\b', re.IGNORECASE),
    re.compile(r'\b\d+\s*(?:feet|ft|foot)\s*(?:\d+\s*(?:inches?|in|ins|\"))?\b', re.IGNORECASE),
    re.compile(r'\b\d+[\'’]\d+(?:\"|”|\b)', re.IGNORECASE)
]

# Matches weight patterns: e.g., "70 kg", "70kg", "154 lbs", "154lbs", "150 pounds"
WEIGHT_PATTERNS = [
    re.compile(r'\b\d+(?:\.\d+)?\s*(?:kg|kgs|kilograms?|lbs?|pounds?)\b', re.IGNORECASE)
]

# Matches age patterns: e.g., "25 years old", "22 yo", "age 30", "i am 28 years of age"
AGE_PATTERNS = [
    re.compile(r'\b\d+\s*(?:years?\s*old|yo|years?\s*of\s*age)\b', re.IGNORECASE),
    re.compile(r'\bi\s*am\s*(\d+)\s*(?:years?\s*old)?\b', re.IGNORECASE),
    re.compile(r'\bmy\s*age\s*(?:is)?\s*(\d+)\b', re.IGNORECASE),
    re.compile(r'\baged?\s*(\d+)\b', re.IGNORECASE)
]

# Matches quantities: numbers or word-numbers followed by a unit of measurement/frequency
QUANTITY_PATTERNS = [
    re.compile(
        r'\b\d+(?:\.\d+)?\s*(?:g|grams?|ml|liters?|l|cups?|servings?|slices?|pieces?|scoops?|minutes?|mins?|hours?|hrs?|times?|kcal|calories?|percent|%|units?|reps?|sets?)\b',
        re.IGNORECASE
    ),
    re.compile(
        r'\b(?:one|two|three|four|five|six|seven|eight|nine|ten)\s*(?:cups?|servings?|slices?|pieces?|scoops?|times?|hours?|minutes?)\b',
        re.IGNORECASE
    ),
    re.compile(r'\b(?:once|twice|thrice)\b', re.IGNORECASE)
]

# =====================================================================
# Keyword Dictionaries
# =====================================================================

GENDER_MAP = {
    "male": ["male", "man", "boy", "gentleman", "masculine"],
    "female": ["female", "woman", "girl", "lady", "feminine"],
    "non-binary": ["nonbinary", "non-binary", "genderqueer", "enby", "agender"]
}

FOOD_GLOSSARY = [
    "apple", "banana", "orange", "grape", "berries", "strawberry", "blueberry", "fruit",
    "rice", "brown rice", "white rice", "oats", "oatmeal", "quinoa", "pasta", "bread",
    "chicken", "chicken breast", "turkey", "beef", "steak", "pork", "fish", "salmon", "tuna",
    "egg", "eggs", "egg white", "egg whites", "tofu", "paneer", "tempeh", "beans", "lentils",
    "broccoli", "spinach", "kale", "lettuce", "cucumber", "tomato", "vegetable", "veggies",
    "milk", "yogurt", "greek yogurt", "cheese", "cottage cheese", "butter", "olive oil",
    "peanut butter", "almond butter", "nuts", "almonds", "walnuts", "avocado",
    "protein shake", "protein bar", "whey protein", "smoothie", "salad", "soup"
]

EXERCISE_GLOSSARY = [
    "running", "jogging", "walking", "brisk walking", "cycling", "swimming", "rowing",
    "cardio", "hiit", "tabata", "aerobics", "jump rope", "skipping",
    "squat", "squats", "pushup", "pushups", "push-up", "push-ups",
    "pullup", "pullups", "pull-up", "pull-ups", "chinup", "chinups",
    "deadlift", "deadlifts", "bench press", "overhead press", "bicep curl", "tricep dip",
    "plank", "planks", "lunge", "lunges", "crunches", "situps", "sit-ups",
    "weightlifting", "lifting weights", "strength training", "calisthenics",
    "yoga", "stretching", "pilates", "zumba"
]

FITNESS_GOAL_MAP = {
    "weight_loss": [
        "lose weight", "weight loss", "fat loss", "burn fat", "shed weight",
        "getting leaner", "slimming down", "dieting"
    ],
    "muscle_gain": [
        "gain muscle", "muscle gain", "build muscle", "bulk up", "bulking",
        "muscle growth", "get bigger", "hypertrophy", "strength gain"
    ],
    "endurance": [
        "improve stamina", "improve endurance", "stamina", "run longer",
        "cardio fitness", "conditioning"
    ],
    "maintenance": [
        "maintain weight", "weight maintenance", "stay fit", "stay active",
        "maintain my weight", "healthy lifestyle"
    ]
}


def extract_entities(text: str) -> Dict[str, Any]:
    """Analyze text input and extract health/fitness related entities.

    Uses regex patterns for physical metrics and quantities, and keyword matching
    for categories like gender, food names, exercises, and fitness goals.

    Parameters
    ----------
    text : str
        The raw user input.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing:
        - height (str or None)
        - weight (str or None)
        - age (int or None)
        - gender (str or None)
        - food_names (list of str)
        - exercise_names (list of str)
        - quantities (list of str)
        - fitness_goals (list of str)
    """
    entities = {
        "height": None,
        "weight": None,
        "age": None,
        "gender": None,
        "food_names": [],
        "exercise_names": [],
        "quantities": [],
        "fitness_goals": [],
        "activity_level": None,
        "water_intake": None
    }

    if not text:
        return entities

    text_lower = text.lower()

    # 1. Height Extraction
    for pattern in HEIGHT_PATTERNS:
        match = pattern.search(text)
        if match:
            entities["height"] = match.group(0).strip()
            break

    # 2. Weight Extraction
    for pattern in WEIGHT_PATTERNS:
        match = pattern.search(text)
        if match:
            entities["weight"] = match.group(0).strip()
            break

    # 3. Age Extraction
    for pattern in AGE_PATTERNS:
        match = pattern.search(text)
        if match:
            # Check if there is a capture group for age digits
            if len(match.groups()) > 0 and match.group(1):
                try:
                    entities["age"] = int(match.group(1))
                except ValueError:
                    pass
            else:
                # Extract digits from the whole matched string
                digits = re.findall(r'\d+', match.group(0))
                if digits:
                    entities["age"] = int(digits[0])
            if entities["age"] is not None:
                break

    # 4. Gender Extraction (Keyword matching)
    from nlp.preprocessor import preprocess_keywords
    kw_text = preprocess_keywords(text)

    for gender_label, keywords in GENDER_MAP.items():
        for kw in keywords:
            kw_clean = preprocess_keywords(kw)
            # Match keywords as whole words
            kw_pattern = re.compile(rf'\b{re.escape(kw_clean)}\b', re.IGNORECASE)
            if kw_pattern.search(kw_text):
                entities["gender"] = gender_label
                break
        if entities["gender"]:
            break

    # 5. Food Name Extraction (Keyword matching)
    for food in FOOD_GLOSSARY:
        food_clean = preprocess_keywords(food)
        # Match as whole words/phrases
        food_pattern = re.compile(rf'\b{re.escape(food_clean)}s?\b', re.IGNORECASE)
        if food_pattern.search(kw_text):
            # Check for duplication
            if food not in entities["food_names"]:
                entities["food_names"].append(food)

    # 6. Exercise Name Extraction (Keyword matching)
    for exercise in EXERCISE_GLOSSARY:
        exercise_clean = preprocess_keywords(exercise)
        # Match as whole words/phrases
        ex_pattern = re.compile(rf'\b{re.escape(exercise_clean)}s?\b', re.IGNORECASE)
        if ex_pattern.search(kw_text):
            if exercise not in entities["exercise_names"]:
                entities["exercise_names"].append(exercise)

    # 7. Quantities Extraction (Regex)
    for pattern in QUANTITY_PATTERNS:
        matches = pattern.findall(text)
        for m in matches:
            m_clean = m.strip()
            if m_clean not in entities["quantities"]:
                entities["quantities"].append(m_clean)

    # 8. Fitness Goal Extraction (Phrase keyword matching)
    for goal_label, keywords in FITNESS_GOAL_MAP.items():
        for kw in keywords:
            kw_clean = preprocess_keywords(kw)
            # Goal matching might be short phrases
            if kw_clean in kw_text:
                if goal_label not in entities["fitness_goals"]:
                    entities["fitness_goals"].append(goal_label)

    # 9. Activity Level Extraction (Keyword matching)
    activity_keywords = {
        "sedentary": ["sedentary", "no exercise", "couch potato", "sit all day"],
        "lightly active": ["lightly active", "light exercise", "walk a bit"],
        "moderately active": ["moderately active", "moderate exercise", "3-5 days gym", "gym 3 times"],
        "very active": ["very active", "highly active", "gym daily", "active lifestyle", "heavy exercise"]
    }
    for act_label, keywords in activity_keywords.items():
        for kw in keywords:
            if kw in text_lower:
                entities["activity_level"] = act_label
                break
        if entities["activity_level"]:
            break

    # 10. Water Intake Extraction (Contextual Quantity matching)
    if "water" in text_lower or "drink" in text_lower or "pina" in text_lower or "piya" in text_lower:
        for qty in entities["quantities"]:
            if any(unit in qty.lower() for unit in ["liter", "litre", "cup", "ml", "oz", "glass", "pina", "piya"]):
                entities["water_intake"] = qty
                break

    return entities
