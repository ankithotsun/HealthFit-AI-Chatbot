"""
HealthFit AI Chatbot — Feedback Data Model

Defines the dataclass DTO for user feedback entries.

Classes
-------
FeedbackEntry
    Represents a thumbs-up or thumbs-down rating linked to
    a specific chat exchange.
"""

from dataclasses import dataclass, asdict


@dataclass
class FeedbackEntry:
    """A user's feedback on a specific bot response.

    Attributes
    ----------
    chat_id : int
        Foreign key linking to the chat_history record that
        the user is rating.
    rating : int
        Binary rating: 1 = thumbs up, 0 = thumbs down.
    id : int or None
        Database primary key, set after insertion.
    timestamp : str
        ISO-format timestamp, set by the database on insert.
    """

    chat_id: int
    rating: int
    id: int = None
    timestamp: str = ""

    def to_dict(self) -> dict:
        """Convert to a plain dictionary for JSON serialization."""
        return asdict(self)
