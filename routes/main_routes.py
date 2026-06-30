"""
HealthFit AI Chatbot — Main Routes

Serves the frontend page and provides the health check
endpoint for monitoring.

Endpoints
---------
GET /
    Render the chat interface page. Returns a placeholder
    JSON response until the frontend templates are built.

GET /api/health
    Returns application health status, version, and
    uptime metadata. Useful for monitoring and verifying
    that the server is running.
"""

from datetime import datetime, timezone

from flask import Blueprint, jsonify, current_app, render_template

# Record server start time for uptime calculation
_server_start_time = datetime.now(timezone.utc)

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def index():
    """Serve the main chat interface page.

    Returns the rendered index.html template when the
    frontend is built. Until then, returns a JSON welcome
    message so the route can be verified.

    Returns
    -------
    Response
        HTML page (200) or JSON placeholder.
    """
    try:
        return render_template("index.html")
    except Exception:
        # Template does not exist yet — return JSON placeholder
        return jsonify({
            "message": "HealthFit AI Chatbot backend is running.",
            "note": "Frontend template not yet implemented.",
            "endpoints": {
                "health": "GET /api/health",
                "chat": "POST /api/chat",
                "history": "GET /api/history?session_id=<id>",
                "delete_history": "DELETE /api/history",
                "feedback": "POST /api/feedback"
            }
        }), 200


@main_bp.route("/api/health", methods=["GET"])
def health_check():
    """Return the application health status.

    Provides a quick way to verify the server is running
    and responsive. Includes app name, version, environment,
    server status, and uptime.

    Returns
    -------
    Response
        JSON with health metadata (200).
    """
    now = datetime.now(timezone.utc)
    uptime_seconds = (now - _server_start_time).total_seconds()

    return jsonify({
        "status": "healthy",
        "app_name": current_app.config.get("APP_NAME",
                                            "HealthFit AI Chatbot"),
        "version": current_app.config.get("APP_VERSION", "1.0.0"),
        "environment": current_app.config.get("ENV", "development"),
        "uptime_seconds": round(uptime_seconds, 2),
        "timestamp": now.isoformat()
    }), 200
