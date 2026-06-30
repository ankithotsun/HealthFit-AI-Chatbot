# CHAPTER 16: SYSTEM DESIGN

System design translates logical requirements into a structured, executable software model. This chapter presents the architectural design, Data Flow Diagrams (DFD), and UML class and sequence diagrams for **HealthFit AI**.

## 16.1 System Architecture

The architecture of HealthFit AI separates concerns into three distinct layers:
1. **Presentation Layer (Frontend UI)**: Handles user interaction, manages local session states, displays dynamic badges, and formats bot responses.
2. **Application Layer (Flask Controller & NLP Services)**: Manages API routes, executes preprocessing pipelines, evaluates ML classifications, and merges multi-intent templates.
3. **Data Persistence Layer (SQLite Database & Model Files)**: Persists session metrics, feedback audits, chat transcripts, and houses the static pre-trained Joblib model files.

```mermaid
graph LR
    subgraph Presentation Layer
        UI[Browser UI: HTML5/CSS3/JS]
    end

    subgraph Application Layer
        Controller[chat_controller.py]
        NLP[nlp_service.py]
        Classifier[classifier.py]
        Prep[preprocessor.py]
    end

    subgraph Data Layer
        DB[(SQLite Database)]
        Models[Joblib Model Files]
    end

    UI <-->|JSON Requests / Responses| Controller
    Controller <--> NLP
    NLP <--> Classifier
    Classifier <--> Prep
    Classifier <--> Models
    NLP <--> DB
```

## 16.2 Data Flow Diagrams (DFD)

Data Flow Diagrams track how data moves through the system.

### DFD Level 0 (Context Level Diagram)

```mermaid
graph TD
    User((User)) <-->|1. Input Message / 4. Chat Response| System[HealthFit AI System]
    Admin((Administrator)) <-->|2. Retrain Command / 3. Model Logs| System
```

### DFD Level 1 (Operational DFD)

```mermaid
graph TD
    User((User)) -->|Input Message| P1[Preprocess Input]
    P1 -->|Clean Text| P2[Predict Intent]
    P2 -->|Intent Tag| P3[Formulate Response]
    P3 -->|Write Log| D1[(SQLite DB)]
    P3 -->|Calculations| P4[Process Calculators]
    P4 -->|Update Badges| User
    P3 -->|Final Text| User
```

### DFD Level 2 (NLP Classification Details)

```mermaid
graph TD
    Input[Raw Text] --> P2_1[Spelling Correction - RapidFuzz]
    P2_1 --> P2_2[Vocabulary Overlap Guard]
    P2_2 -- Has Overlap --> P2_3[TF-IDF Transformation]
    P2_2 -- Zero Overlap --> Fallback[Instant Fallback Route]
    P2_3 --> P2_4[Logistic Regression Score]
    P2_4 --> P2_5[Keyword Boost Evaluation]
    P2_5 --> P2_6[Normalization & Multi-Intent Scan]
    P2_6 --> Output[Selected Intent List]
```

## 16.3 UML Diagrams

UML diagrams model structural class relationships and chronological service messaging sequences.

### UML Class Diagram

```mermaid
classDiagram
    class DatabaseManager {
        +init_db(db_path)
        +save_message(session_id, sender, message, intent, confidence, db_path)
        +get_chat_history(session_id, limit, db_path)
        +save_session_profile(session_id, profile, db_path)
        +get_session_profile(session_id, db_path)
        +save_feedback(message_id, rating, db_path)
    }

    class TextPreprocessor {
        +preprocess_classifier(text)
        +preprocess_keywords(text)
        +correct_spelling(text)
        +normalize_synonyms(tokens)
    }

    class Classifier {
        +load_model(vectorizer_path, model_path)
        +predict_intent(text, vectorizer, model, threshold, raw_text)
        -KEYWORD_BOOST_MAP
    }

    class ChatController {
        +process_message(message, session_id, db_path, confidence_threshold)
    }

    class NLPService {
        +analyse_message(message, confidence_threshold, context_history, session_id, db_path)
        +compose_response(intents, entities, profile)
    }

    ChatController --> NLPService
    NLPService --> Classifier
    Classifier --> TextPreprocessor
    NLPService --> DatabaseManager
```

### UML Sequence Diagram (Message Request)

```mermaid
sequenceDiagram
    autonumber
    actor User as Browser UI
    participant C as chat_controller.py
    participant N as nlp_service.py
    participant CL as classifier.py
    participant DB as db_manager.py

    User->>C: POST /api/chat {message, session_id}
    C->>DB: get_session_profile(session_id)
    DB-->>C: profile_data
    C->>DB: get_chat_history(session_id, limit=3)
    DB-->>C: context_history
    C->>N: analyse_message(message, history, profile)
    N->>CL: predict_intent(cleaned_text, raw_text)
    CL-->>N: intent_list, confidence
    N->>N: Run Calculators & Format Templates
    N->>DB: save_session_profile(session_id, updated_profile)
    N->>DB: save_message(session_id, sender, message, intent, confidence)
    N-->>C: final_response, entities, updated_profile
    C-->>User: JSON response {response, intent, entities}
```
