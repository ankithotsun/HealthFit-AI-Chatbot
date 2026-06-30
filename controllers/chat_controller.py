"""
HealthFit AI Chatbot — Chat Controller

Orchestrates the chat pipeline by coordinating between the
NLP service layer and the database layer. This controller
is HTTP-agnostic — it works with plain Python objects, not
Flask request/response objects.

Flow
----
    Route (HTTP) → Controller → NLP Service → Database
                 ← ChatResponse ←

Functions
---------
process_message(message, session_id, db_path, threshold)
    Run the full chat pipeline and return a ChatResponse.
get_chat_history(session_id, db_path, limit)
    Retrieve conversation history for a session.
clear_chat_history(session_id, db_path)
    Delete all chat records for a session.
"""

from models.chat_model import ChatMessage, ChatResponse
from services.nlp_service import analyse_message
from utils.db_manager import save_chat, get_history, clear_session


def process_message(message: str, session_id: str,
                    db_path: str,
                    confidence_threshold: float = 0.45) -> ChatResponse:
    """Process a user message through the full pipeline.

    Steps:
    1. Retrieve the previous 3 user messages from the database as context.
    2. Send the message and context to the NLP service for analysis.
    3. Build a ChatMessage DTO with the results.
    4. Persist the exchange to the database.
    5. Return a ChatResponse DTO to the route layer.

    Parameters
    ----------
    message : str
        The raw text typed by the user.
    session_id : str
        The conversation session identifier.
    db_path : str
        Path to the SQLite database file.
    confidence_threshold : float, optional
        Minimum classifier confidence to accept an intent.
        Default is 0.45.

    Returns
    -------
    ChatResponse
        Contains the bot's reply, detected intent,
        confidence score, and the database record ID.
    """
    # Fetch recent context history (up to last 3 exchanges)
    context_history = []
    try:
        context_history = get_chat_history(session_id, db_path, limit=3)
    except Exception:
        pass

    # Step 1: Analyse the message via the NLP service (passing context history and session details)
    intent, confidence, response, entities = analyse_message(
        message=message,
        confidence_threshold=confidence_threshold,
        context_history=context_history,
        session_id=session_id,
        db_path=db_path
    )

    # Step 2: Build the ChatMessage DTO for persistence
    chat_record = ChatMessage(
        session_id=session_id,
        user_message=message,
        detected_intent=intent,
        confidence_score=round(confidence, 4),
        bot_response=response
    )

    # Step 3: Save to the database and get the record ID
    chat_id = save_chat(db_path, chat_record)

    # Step 4: Build and return the API response DTO
    return ChatResponse(
        response=response,
        intent=intent,
        confidence=round(confidence, 4),
        chat_id=chat_id,
        entities=entities
    )


def get_chat_history(session_id: str, db_path: str,
                     limit: int = 50) -> list[dict]:
    """Retrieve the chat history for a conversation session.

    Parameters
    ----------
    session_id : str
        The session identifier to query.
    db_path : str
        Path to the SQLite database file.
    limit : int, optional
        Maximum number of messages to return. Default is 50.

    Returns
    -------
    list[dict]
        A list of chat exchange dictionaries, ordered by
        timestamp ascending.
    """
    return get_history(db_path, session_id, limit)


def clear_chat_history(session_id: str, db_path: str) -> int:
    """Delete all chat records for a session.

    Associated feedback records are also removed via the
    ON DELETE CASCADE foreign key constraint.

    Parameters
    ----------
    session_id : str
        The session identifier whose records to delete.
    db_path : str
        Path to the SQLite database file.

    Returns
    -------
    int
        The number of chat records deleted.
    """
    return clear_session(db_path, session_id)
