"""
HealthFit AI Chatbot — Feedback Controller

Handles the business logic for user feedback submissions.
Validates that the referenced chat record exists before
saving feedback. HTTP-agnostic — works with plain Python
objects.

Functions
---------
submit_feedback(chat_id, rating, db_path)
    Validate and save user feedback for a chat exchange.
"""

from models.feedback_model import FeedbackEntry
from utils.db_manager import save_feedback, chat_exists


def submit_feedback(chat_id: int, rating: int,
                    db_path: str) -> dict:
    """Validate and persist user feedback.

    Performs two validations before saving:
    1. The rating must be 0 (thumbs down) or 1 (thumbs up).
    2. The referenced chat_id must exist in the database.

    Parameters
    ----------
    chat_id : int
        The primary key of the chat_history record to rate.
    rating : int
        Binary rating: 1 = thumbs up, 0 = thumbs down.
    db_path : str
        Path to the SQLite database file.

    Returns
    -------
    dict
        On success: {"status": "saved", "feedback_id": <int>}
        On failure: {"status": "error", "message": "<reason>"}
    """
    # Validate rating value
    if rating not in (0, 1):
        return {
            "status": "error",
            "message": "Rating must be 0 (thumbs down) or 1 (thumbs up)."
        }

    # Validate that the chat record exists
    if not chat_exists(db_path, chat_id):
        return {
            "status": "error",
            "message": f"Chat record with id {chat_id} not found."
        }

    # Build the feedback DTO and save
    feedback = FeedbackEntry(chat_id=chat_id, rating=rating)
    feedback_id = save_feedback(db_path, feedback)

    return {
        "status": "saved",
        "feedback_id": feedback_id
    }
