# INSTALLATION & CONFIGURATION GUIDE: HEALTHFIT AI

This guide provides step-by-step instructions to set up, train, and run **HealthFit AI** locally.

## Prerequisites
Before starting, ensure your system has **Python 3.9** or higher installed.

---

## Step 1: Clone the Repository & Setup Virtual Environment
Open your terminal or command prompt and execute:

```bash
# 1. Clone or navigate to the repository directory
cd /Users/ankit/Documents/HealthFit-AI-Chatbot

# 2. Create a clean virtual environment named 'venv'
python3 -m venv venv

# 3. Activate the virtual environment
# On macOS / Linux:
source venv/bin/activate
# On Windows (cmd):
# venv\Scripts\activate.bat
```

---

## Step 2: Install Package Dependencies
Install all required libraries using `pip`:

```bash
# Update pip to the latest version
pip install --upgrade pip

# Install dependencies
pip install Flask scikit-learn nltk joblib rapidfuzz pytest numpy
```

*Note: The NLTK corpora (punkt, stopwords, wordnet) will be downloaded automatically by the preprocessor module during the first run.*

---

## Step 3: Compile Intents Dataset & Train Model
The statistical classifier must be trained on the intents dataset to build the TF-IDF feature vocabulary:

```bash
# 1. (Optional) Compile and expand the intents database
python3 data/generate_intents.py

# 2. Train the Logistic Regression classifier
python3 train_model.py
```

This will run preprocessing and validation evaluations, saving:
* `models_ml/tfidf_vectorizer.pkl`
* `models_ml/trained_model.pkl`

---

## Step 4: Run the Testing Suite
Verify that all unit and integration assertions pass successfully:

```bash
python3 -m pytest tests/test_nlp.py
```

---

## Step 5: Start the Flask Server
Launch the local web server:

```bash
python3 app.py
```

Open your browser and navigate to:
**`http://127.0.0.1:5000`**
The HealthFit AI interface is now active and ready for use.
