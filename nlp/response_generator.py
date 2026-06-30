"""
HealthFit AI Chatbot — Response Generator

This module maps a classified intent label to an appropriate
response string. It loads the intent dataset (intents.json)
and randomly selects from the response pool for each intent,
ensuring variety in the chatbot's replies.

Design Decisions
----------------
- Responses are stored in intents.json, not hardcoded here.
  This separates data from logic — adding new responses only
  requires editing the JSON file, not the Python code.

- Random selection from the response pool prevents the bot
  from always giving the same reply to the same question,
  which makes the conversation feel more natural.

- The response map is built once at module load time from the
  JSON file. This avoids repeated file I/O on every request.

Functions
---------
load_responses(intents_path)
    Load and parse the intents JSON file into a response map.
get_response(intent_tag, response_map)
    Return a randomly selected response for the given intent.
get_fallback_response(response_map)
    Return a safe fallback response for unrecognised queries.
"""

import json
import random
import os


# ============================================================
# Response Map Loading
# ============================================================

def load_responses(intents_path: str) -> dict:
    """Load the intents file and build an intent → responses map.

    Reads the intents.json file and constructs a dictionary
    where each key is an intent tag and the value is the list
    of possible response strings for that intent.

    Parameters
    ----------
    intents_path : str
        Absolute path to the intents.json data file.

    Returns
    -------
    dict[str, list[str]]
        A dictionary mapping intent tag strings to lists of
        response strings.

    Raises
    ------
    FileNotFoundError
        If the intents file does not exist at the given path.
    ValueError
        If the file is not valid JSON or has unexpected format.

    Example (structure of returned dict)
    -------------------------------------
    {
        "greeting": ["Hello! How can I help you?", "Hi there!"],
        "workout_beginner": ["Here is a beginner plan...", ...],
        "fallback": ["I did not understand that...", ...]
    }
    """
    if not os.path.exists(intents_path):
        raise FileNotFoundError(
            f"Intents file not found at: {intents_path}"
        )

    with open(intents_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid JSON in intents file: {exc}"
            ) from exc

    # Build the response map: {tag: [response1, response2, ...]}
    response_map = {}
    for intent in data.get("intents", []):
        tag = intent.get("tag", "").strip()
        responses = intent.get("responses", [])
        if tag and responses:
            response_map[tag] = responses

    return response_map


# ============================================================
# Response Retrieval
# ============================================================

def get_response(intent_tag: str, response_map: dict) -> str:
    """Return a randomly selected response for the given intent.

    Picks one response at random from the list associated with
    the intent tag. Random selection introduces variety so the
    chatbot does not give the same answer every time.

    If the intent tag is not found in the response map (which
    should not happen in normal operation, but is handled
    defensively), the fallback response is returned.

    Parameters
    ----------
    intent_tag : str
        The intent label returned by the classifier
        (e.g., 'workout_beginner', 'bmi', 'fallback').
    response_map : dict[str, list[str]]
        The mapping from intent tags to response lists,
        as returned by load_responses().

    Returns
    -------
    str
        A randomly selected response string for the intent.

    Example
    -------
    >>> response_map = {"greeting": ["Hello!", "Hi there!"]}
    >>> get_response("greeting", response_map)
    'Hi there!'   # or 'Hello!' — random each call
    """
    responses = response_map.get(intent_tag)

    if not responses:
        # Intent not in map — fall back to the generic fallback
        return get_fallback_response(response_map)

    # random.choice selects one item uniformly at random
    return random.choice(responses)


def get_fallback_response(response_map: dict) -> str:
    """Return a safe fallback response for unrecognised queries.

    Used when the classifier confidence is below the threshold,
    or when the predicted intent has no responses in the map.

    Parameters
    ----------
    response_map : dict[str, list[str]]
        The response map, which should contain a 'fallback' key.

    Returns
    -------
    str
        A randomly selected fallback response string.
        Returns a hardcoded default if 'fallback' is missing
        from the response map.
    """
    fallback_responses = response_map.get("fallback")

    if fallback_responses:
        return random.choice(fallback_responses)

    # Ultimate hardcoded fallback in case the JSON is missing
    # the fallback intent entirely.
    return (
        "I am sorry, I did not understand that. Please try "
        "asking about workouts, diet, BMI, hydration, sleep, "
        "or general fitness topics."
    )
