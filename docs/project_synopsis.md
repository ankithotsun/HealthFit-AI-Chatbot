# PROJECT SYNOPSIS: HEALTHFIT AI

## 1. Title of the Project
**HealthFit AI: An Intelligent Chatbot for Health and Fitness Guidance using Hybrid NLP Techniques**

## 2. Introduction & Background
With rising urbanization and sedentary work cultures, lifestyle-related health conditions (obesity, hypertension, diabetes) have increased globally. Access to professional fitness trainers and dietitians is often costly and inaccessible. While generic search engines contain vast information, they lack personalization. **HealthFit AI** addresses this gap by offering a lightweight, offline-first, conversational chatbot that provides tailored diet, workout, and metric calculations in real-time.

## 3. Objective of the Project
- To classify fitness queries into 34 distinct intents with over 95% validation accuracy.
- To store and retrieve user physical profiles (weight, height, age, gender, goal) across chat turns.
- To handle multi-intent inputs (e.g., *"suggest a diet and squats guide"*) and merge responses.
- To correct user typos (RapidFuzz $\ge 90\%$) and normalize synonyms using WordNet without stopword-collision issues.
- To provide guided fallbacks for out-of-scope interactions and warnings for emergency clinical inputs.

## 4. System Architecture
HealthFit AI separates concerns into:
- **Presentation Layer**: A mobile-responsive web interface built with HTML5, CSS3, and Bootstrap 5.
- **Application Layer**: A Flask web server routing requests, executing NLP classification (TF-IDF + Logistic Regression), and running metric calculators (BMI, BMR).
- **Data Layer**: An SQLite database engine persisting chat history transcripts, session profiles, and feedback ratings.

## 5. Software & Hardware Specifications
* **Programming Language**: Python 3.9+
* **Framework**: Flask 3.0.x
* **Machine Learning**: scikit-learn, NLTK, joblib
* **String Distance**: rapidfuzz
* **Database**: SQLite 3
* **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5

## 6. Project Deliverables
- Fully functional conversational web app.
- Automated ML dataset generator & training script.
- Persistent database schema for session tracking & feedback.
- Automated testing suite & validation reports.
