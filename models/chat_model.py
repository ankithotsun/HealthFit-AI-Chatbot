"""
HealthFit AI Chatbot — Chat Data Models

Defines dataclass DTOs for chat-related data flowing through
the application layers.

Classes
-------
ChatMessage
    Represents a complete chat exchange stored in the database.
ChatResponse
    Represents the JSON response returned to the frontend.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class ChatMessage:
    """A single chat exchange between the user and the bot.

    This object is created by the controller after the NLP
    service processes a user query, and is passed to the
    database manager for persistence.

    Attributes
    ----------
    session_id : str
        Groups messages into a single conversation session.
    user_message : str
        The original text typed by the user.
    detected_intent : str
        The intent label returned by the classifier.
    confidence_score : float
        The classifier's confidence in the detected intent
        (range 0.0 to 1.0).
    bot_response : str
        The response text sent back to the user.
    id : int or None
        Database primary key, set after insertion.
    timestamp : str
        ISO-format timestamp, set by the database on insert.
    """

    session_id: str
    user_message: str
    detected_intent: str
    confidence_score: float
    bot_response: str
    id: int = None
    timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )

    def to_dict(self) -> dict:
        """Convert to a plain dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class ChatResponse:
    """The JSON payload returned to the frontend after a chat.

    Attributes
    ----------
    response : str
        The bot's reply text.
    intent : str
        The classified intent label.
    confidence : float
        Classifier confidence score.
    chat_id : int
        Database ID of the saved chat record, used for
        linking feedback.
    entities : dict, optional
        Key-value pairs of extracted entities (e.g. age, weight, height).
    """

    response: str
    intent: str
    confidence: float
    chat_id: int
    entities: dict = None

    def to_dict(self) -> dict:
        """Convert to a plain dictionary for JSON serialization."""
        return asdict(self)

