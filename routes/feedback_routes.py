"""
HealthFit AI Chatbot — Feedback Routes

RESTful API endpoint for submitting user feedback on
bot responses. Each feedback entry is a thumbs-up (1)
or thumbs-down (0) linked to a specific chat exchange.

Endpoints
---------
POST /api/feedback
    Submit a rating for a specific chat response.
"""

from flask import Blueprint, request, jsonify, current_app

from controllers.feedback_controller import submit_feedback

feedback_bp = Blueprint("feedback", __name__)


@feedback_bp.route("/api/feedback", methods=["POST"])
def feedback():
    """Submit user feedback for a bot response.

    Expects a JSON body with:
    - chat_id (int, required): The ID of the chat exchange
      being rated.
    - rating (int, required): 1 for thumbs up, 0 for
      thumbs down.

    Returns
    -------
    Response
        201: JSON confirming feedback was saved.
        400: JSON with error details if validation fails.
        500: JSON with error details on server failure.

    Example Request
    ---------------
    POST /api/feedback
    Content-Type: application/json

    {
        "chat_id": 42,
        "rating": 1
    }

    Example Response (Success)
    --------------------------
    {
        "status": "saved",
        "feedback_id": 7
    }

    Example Response (Error)
    ------------------------
    {
        "status": "error",
        "message": "Chat record with id 999 not found."
    }
    """
    # Parse JSON body
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

    # Extract and validate fields
    chat_id = data.get("chat_id")
    rating = data.get("rating")

    if chat_id is None:
        return jsonify({
            "error": "The 'chat_id' field is required."
        }), 400

    if not isinstance(chat_id, int) or chat_id < 1:
        return jsonify({
            "error": "The 'chat_id' must be a positive integer."
        }), 400

    if rating is None:
        return jsonify({
            "error": "The 'rating' field is required."
        }), 400

    if rating not in (0, 1):
        return jsonify({
            "error": "The 'rating' must be 0 (thumbs down) "
                     "or 1 (thumbs up)."
        }), 400

    # Delegate to the controller
    try:
        db_path = current_app.config["DATABASE_PATH"]

        result = submit_feedback(
            chat_id=chat_id,
            rating=rating,
            db_path=db_path
        )

        if result["status"] == "error":
            return jsonify(result), 400

        return jsonify(result), 201

    except Exception as exc:
        current_app.logger.error(
            "Error saving feedback: %s", str(exc)
        )
        return jsonify({
            "error": "An internal error occurred while "
                     "saving your feedback.",
            "details": str(exc)
        }), 500
