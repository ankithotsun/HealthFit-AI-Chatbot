# TECHNICAL MANUAL: HEALTHFIT AI CHATBOT

This manual provides low-level developer documentation detailing the code implementation, classes, algorithms, and training procedures of **HealthFit AI**.

## 1. Modular Architecture Overview

```
                        +----------------------------+
                        |         app.py             |
                        | (Flask Routing & API)      |
                        +--------------+-------------+
                                       |
                        +--------------v-------------+
                        |  chat_controller.py        |
                        | (Session/History Broker)   |
                        +--------------+-------------+
                                       |
                        +--------------v-------------+
                        |       nlp_service.py       |
                        | (Calculator Engine)        |
                        +--------------+-------------+
                                       |
                        +--------------v-------------+
                        |        classifier.py       |
                        | (Inference & Boosting)     |
                        +--------------+-------------+
                                       |
                        +--------------v-------------+
                        |       preprocessor.py      |
                        | (Fuzzy & WordNet Cleaning) |
                        +----------------------------+
```

## 2. Low-Level Component Details

### A. Preprocessor (`nlp/preprocessor.py`)
Provides two main functions to process text strings:
- `preprocess_classifier(text)`: Lowercases, removes punctuation, and normalizes whitespace. It **retains stopwords** so that syntax patterns (such as greetings and conversational queries) can be recognized by TF-IDF.
- `preprocess_keywords(text)`: Standardizes spelling, expands contractions, removes stopwords, lemmatizes terms, and applies WordNet synonym maps to extract key concepts (e.g. mapping "adipose" or "obese" to the concept "fat").
- **Synonym Blacklist (`_SYNONYM_BLACKLIST`)**: Prevents common words like "mass" or "strength" from undergoing synonym expansion, avoiding collisions (e.g., preventing "Body Mass Index" from mapping to "bulk" or "strength training" from mapping to "muscle").

### B. NLP Classifier Engine (`nlp/classifier.py`)
- **Model Loading**: `load_model(vectorizer_path, model_path)` loads pre-trained vectorizers and classifiers from `.pkl` files using `joblib`.
- **Vocabulary Overlap Guard**: Checks if the query words exist in the vectorizer vocabulary. If there is zero overlap, it bypasses Logistic Regression and returns `fallback` immediately, filtering out out-of-scope inputs.
- **Keyword Boosting**: Evaluates whether keywords associated with a class are present in the raw input. If found, it boosts the class's raw probability by `+1.5` before soft-max re-normalization.
- **Multi-Intent Verification**: Scans the normalized probability distribution. If any secondary intent score is $\ge 0.38$, it returns a list containing both the primary and secondary intents.

### C. Database Manager (`utils/db_manager.py`)
- Employs an SQLite connection pool.
- `get_history(session_id, limit)`: Uses `ORDER BY id DESC LIMIT ?` to retrieve the most recent rows from the database. It then reverses the records in Python to maintain chronological order, providing a sliding context history.
- `save_session_profile(session_id, profile)`: Persists height, weight, age, gender, and fitness goal variables in the `session_profile` table using an upsert statement (`INSERT OR REPLACE`).

## 3. Extending the Chatbot: How to Add a New Intent

To introduce a new intent class (e.g., `cardio_hiit`):
1. **Define the Intent Blueprint**:
   Open `data/generate_intents.py`. Append a new dictionary to the `BLUEPRINTS` list:
   ```python
   {
       "tag": "cardio_hiit",
       "bases": ["hiit workout", "high intensity intervals", "sprints training", "hiit routine"],
       "responses": [
           "HIIT training alternates high-intensity exercises with rest. Try sprinting for 30s followed by 60s walking.",
           "Perform 4-5 rounds of intervals to boost cardiovascular health and calorie burn."
       ]
   }
   ```
2. **Add Boost Keywords**:
   Open `nlp/classifier.py`. Add the corresponding keywords to `KEYWORD_BOOST_MAP`:
   ```python
   "cardio_hiit": ["hiit", "interval training", "intervals", "sprints"]
   ```
3. **Recompile & Retrain**:
   Execute the dataset generator and retraining pipeline:
   ```bash
   python3 data/generate_intents.py
   python3 train_model.py
   ```
4. **Verify**:
   Run the test runner to ensure the model compiles, validates, and runs without issues.
