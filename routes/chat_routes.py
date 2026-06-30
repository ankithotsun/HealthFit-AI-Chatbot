"""
HealthFit AI Chatbot — Chat Routes

RESTful API endpoints for the core chat functionality.
All routes use the /api/ prefix for clean separation
from page routes.

Endpoints
---------
POST /api/chat
    Accept a user message, process it through the NLP
    pipeline, and return the bot's response.

GET /api/history
    Retrieve the conversation history for a session.

DELETE /api/history
    Clear all conversation history for a session.
"""

from flask import Blueprint, request, jsonify, current_app

from controllers.chat_controller import (
    process_message,
    get_chat_history,
    clear_chat_history,
)

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/api/chat", methods=["POST"])
def chat():
    """Process a user message and return a bot response.

    Expects a JSON body with:
    - message (str, required): The user's text query.
    - session_id (str, required): Conversation session ID.

    Returns
    -------
    Response
        201: JSON with response, intent, confidence, chat_id.
        400: JSON with error details if validation fails.
        500: JSON with error details on server failure.

    Example Request
    ---------------
    POST /api/chat
    Content-Type: application/json

    {
        "message": "What is a good beginner workout?",
        "session_id": "abc-123"
    }

    Example Response
    ----------------
    {
        "response": "Here's a great beginner routine...",
        "intent": "workout_suggestion",
        "confidence": 0.87,
        "chat_id": 42
    }
    """
    # Parse JSON body
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

    # Extract and validate fields
    message = data.get("message", "").strip()
    session_id = data.get("session_id", "").strip()

    if not message:
        return jsonify({
            "error": "The 'message' field is required and "
                     "cannot be empty."
        }), 400

    if not session_id:
        return jsonify({
            "error": "The 'session_id' field is required and "
                     "cannot be empty."
        }), 400

    # Process through the controller → service → DB pipeline
    try:
        db_path = current_app.config["DATABASE_PATH"]
        threshold = current_app.config["CONFIDENCE_THRESHOLD"]

        result = process_message(
            message=message,
            session_id=session_id,
            db_path=db_path,
            confidence_threshold=threshold
        )

        return jsonify(result.to_dict()), 201

    except Exception as exc:
        current_app.logger.error(
            "Error processing chat message: %s", str(exc)
        )
        return jsonify({
            "error": "An internal error occurred while "
                     "processing your message.",
            "details": str(exc)
        }), 500


@chat_bp.route("/api/history", methods=["GET"])
def history():
    """Retrieve chat history for a conversation session.

    Query Parameters
    ----------------
    session_id : str (required)
        The session identifier to retrieve history for.

    Returns
    -------
    Response
        200: JSON with a list of chat exchanges.
        400: JSON with error if session_id is missing.

    Example Request
    ---------------
    GET /api/history?session_id=abc-123

    Example Response
    ----------------
    {
        "session_id": "abc-123",
        "count": 5,
        "history": [
            {
                "id": 1,
                "user_message": "hello",
                "detected_intent": "greeting",
                "confidence_score": 0.95,
                "bot_response": "Hi there!",
                "timestamp": "2026-06-26T12:00:00"
            },
            ...
        ]
    }
    """
    session_id = request.args.get("session_id", "").strip()

    if not session_id:
        return jsonify({
            "error": "Query parameter 'session_id' is required."
        }), 400

    try:
        db_path = current_app.config["DATABASE_PATH"]
        limit = current_app.config["MAX_HISTORY_LENGTH"]

        messages = get_chat_history(
            session_id=session_id,
            db_path=db_path,
            limit=limit
        )

        return jsonify({
            "session_id": session_id,
            "count": len(messages),
            "history": messages
        }), 200

    except Exception as exc:
        current_app.logger.error(
            "Error fetching chat history: %s", str(exc)
        )
        return jsonify({
            "error": "An internal error occurred while "
                     "retrieving chat history.",
            "details": str(exc)
        }), 500


@chat_bp.route("/api/history", methods=["DELETE"])
def delete_history():
    """Clear all conversation history for a session.

    Expects a JSON body with:
    - session_id (str, required): The session to clear.

    Associated feedback records are automatically removed
    via the ON DELETE CASCADE foreign key constraint.

    Returns
    -------
    Response
        200: JSON confirming deletion with count.
        400: JSON with error if session_id is missing.

    Example Request
    ---------------
    DELETE /api/history
    Content-Type: application/json

    {
        "session_id": "abc-123"
    }

    Example Response
    ----------------
    {
        "status": "cleared",
        "session_id": "abc-123",
        "deleted_count": 12
    }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "error": "Request body must be valid JSON."
        }), 400

    session_id = data.get("session_id", "").strip()

    if not session_id:
        return jsonify({
            "error": "The 'session_id' field is required and "
                     "cannot be empty."
        }), 400

    try:
        db_path = current_app.config["DATABASE_PATH"]

        deleted_count = clear_chat_history(
            session_id=session_id,
            db_path=db_path
        )

        return jsonify({
            "status": "cleared",
            "session_id": session_id,
            "deleted_count": deleted_count
        }), 200

    except Exception as exc:
        current_app.logger.error(
            "Error clearing chat history: %s", str(exc)
        )
        return jsonify({
            "error": "An internal error occurred while "
                     "clearing chat history.",
            "details": str(exc)
        }), 500
