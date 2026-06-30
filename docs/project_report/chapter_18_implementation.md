# CHAPTER 18: IMPLEMENTATION

This chapter details the modular code structure, key software components, packages, and UI layout design implementations for **HealthFit AI**.

## 18.1 Key Modules & Packages

The codebase is organized in an MVC-inspired layout to enforce clear separation of concerns.

```
HealthFit-AI-Chatbot/
│
├── app.py                      # Flask Server Entrypoint & API Route definitions
├── train_model.py              # ML Dataset Compiler & Classifier Retraining Script
│
├── controllers/
│   └── chat_controller.py      # Request parser, history retrieval & orchestrator
│
├── services/
│   └── nlp_service.py          # Dynamic template composer, BMI/BMR/Hydration calculators
│
├── nlp/
│   ├── classifier.py           # joblib model loader, keyword boost maps & multi-intent checks
│   ├── preprocessor.py         # Spelling correction, contraction, stopword, and synonym lemmatizers
│   └── entity_extractor.py     # Regular expression and keyword physical metric parsing
│
├── utils/
│   └── db_manager.py           # SQLite connection pools and table CRUD executions
│
├── templates/
│   └── index.html              # HTML5 Web UI Layout
│
└── static/
    ├── css/
    │   └── style.css           # Vanilla CSS styles, bubbles, typing animations
    └── js/
        └── main.js             # AJAX state orchestrator, UI renders, and profiles
```

### Module Descriptions and Key Operations

1. **`app.py`**:
   Initializes the Flask server, configures static folders, and maps endpoints. Crucial routes include `/api/chat` (receives inputs, invokes the controller), `/api/feedback` (records ratings), and `/api/history` (loads past session turns for the dashboard).
2. **`controllers/chat_controller.py`**:
   The controller acts as the traffic manager. It parses incoming JSON request structures, queries history variables from SQLite, fetches session physical statistics, invokes the NLP analysis service, and formats the output dictionary sent back to `app.py`.
3. **`services/nlp_service.py`**:
   Contains core dynamic template composition logic. If the predicted intent matches calculations (e.g. `bmi`), it extracts current height and weight from the parser, executes Mifflin-St Jeor evaluations, and injects results into text placeholders.
4. **`nlp/classifier.py`**:
   Executes TF-IDF feature projections. Implements keyword boosting maps and checks if secondary intent scores exceed `0.38` to trigger multi-intent responses.
5. **`nlp/preprocessor.py`**:
   Implements text cleaning. Defines `preprocess_classifier` (keeping stopwords to preserve syntactic structure) and `preprocess_keywords` (lemmatizing and resolving synonyms using WordNet).
6. **`utils/db_manager.py`**:
   Encapsulates all SQL statements. Creates tables if missing and provides transaction methods to log chat transcripts, profile variables, and ratings.

## 18.2 UI Layout Design

The frontend user interface is built using a highly aesthetic and responsive design:
- **Responsive Sidebar**: Constructed with Bootstrap grid layouts. The sidebar lists past chat sessions stored in browser `localStorage`, allowing users to create new sessions or clear existing history.
- **Header Avatar Panel**: A pulsing, custom-styled emerald green circular robot icon representing the HealthFit AI assistant, indicating online status.
- **Scrollable Chat Area**: Dynamic chat bubble wrappers. User messages are styled in blue gradients aligned to the right; bot responses are styled in white/glassmorphism templates aligned to the left.
- **Autoscroll & Typing Indicators**: JavaScript monitors panel height and scrolls to bottom on new additions. While waiting for backend responses, a three-dot bobbing typing indicator animation plays.
- **Entity Badges**: Behind the scenes, JavaScript extracts intent tags and metric structures from JSON payloads and renders small badges (e.g., `Weight: 80 kg`, `Primary: hydration`) beneath each message bubble to provide visual feedback.
- **Enter-to-Send & Counter**: Listens for Enter key presses on the input bar (disabling default linebreaks) and features a real-time character counter to prevent excessive inputs.
