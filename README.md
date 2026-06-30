# HealthFit AI — Intelligent Health & Fitness Chatbot

HealthFit AI is an interactive, context-aware chatbot designed to provide personalized diet, exercise, and wellness guidance using a hybrid Natural Language Processing (NLP) framework.

Unlike standard chatbots, HealthFit AI combines a statistical machine learning classifier (TF-IDF + Logistic Regression) with domain-specific keyword boosting, fuzzy spelling correction, and WordNet synonym mapping to deliver highly accurate, safe, and deterministic health advice.

---

## Key Features
* **Hybrid NLP Classification**: 97.65% validation accuracy on a balanced dataset of 34 intents and 2,550 patterns.
* **Persistent Session Profiles**: Automatically stores user height, weight, age, gender, and goals in an SQLite database, dynamically updating UI metrics badges.
* **Dynamic Health Calculators**: Performs instant BMI, BMR, and water requirement calculations based on saved user profiles.
* **Multi-Intent Handling**: Detects compound queries (e.g., *"suggest a diet and squats guide"*) and merges templates into a single response.
* **Context Resolution**: Bypasses classification for follow-up phrases (e.g., *"explain it"*, *"elaborate"*), inheriting the previous conversation's intent.
* **Fuzzy Spelling Correction**: Corrects typographical errors (RapidFuzz $\ge 90\%$) before preprocessing.
* **Vocabulary Overlap Guard**: Instantly rejects out-of-scope queries (e.g. *"who is the president"*), routing them to fallback suggestions.
* **Premium User Interface**: Includes typing indicators, bubble gradients, dynamically updated badges, sidebar session history management, and response rating loops (👍/👎).

---

## System Architecture

```
Presentation Layer (Bootstrap 5, JS) <==> Flask API Controllers (chat_controller.py)
                                                    ||
                                        NLP Engine Services (nlp_service.py)
                                                    ||
                                  Stat Classifier & SQL (SQLite DB, Joblib)
```

---

## Installation & Setup

1. **Clone the Repository**:
   ```bash
   cd /Users/ankit/Documents/HealthFit-AI-Chatbot
   ```
2. **Configure Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate.bat
   ```
3. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install Flask scikit-learn nltk joblib rapidfuzz pytest numpy
   ```
4. **Compile & Train Model**:
   ```bash
   python3 data/generate_intents.py
   python3 train_model.py
   ```
5. **Run Integration Tests**:
   ```bash
   python3 -m pytest tests/test_nlp.py
   ```
6. **Start Flask Server**:
   ```bash
   python3 app.py
   ```

Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## Project Structure
* `app.py`: Flask routes and API definitions.
* `train_model.py`: Model training and metrics validation.
* `controllers/`: Handles request parsing, session loading, and history context.
* `services/`: Houses dynamic calculators and template engines.
* `nlp/`: Code for preprocessing, spelling correction, and classifier predictions.
* `utils/`: Core database connections and CRUD scripts.
* `docs/`: Holds the full project report, manuals, and evaluation metrics.
