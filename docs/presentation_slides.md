# PRESENTATION SLIDES: HEALTHFIT AI CHATBOT

This document outlines the **17 slides** designed for the final-year MCA project evaluation presentation.

---

### SLIDE 1: Title Slide
* **Title**: HealthFit AI: An Intelligent Chatbot for Health and Fitness Guidance using Hybrid NLP Techniques
* **Presenter**: Ankit (MCA Final Year, Chandigarh University)
* **Under the Guidance of**: [Insert Guide Name]
* **Institution**: Department of Computer Applications, Chandigarh University

---

### SLIDE 2: Project Overview
* **Concept**: An interactive virtual wellness companion helping users log metrics, plan workouts, and get dietary advice.
* **Why local NLP?**: Bypasses the latency, cost, and hallucination risks of generative LLMs.
* **Architecture**: Flask backend, SQLite persistence, and Bootstrap 5 responsive frontend.

---

### SLIDE 3: Problem Statement
* Lack of personalized, interactive health advice online.
* User frustration with static, button-only interfaces.
* Handling typographical errors and bilingual Hinglish inputs.
* High computational footprint of deep learning transformer models.

---

### SLIDE 4: Objectives
* Build a statistical classifier (TF-IDF + Logistic Regression) with validation accuracy > 95%.
* Implement local SQLite-based dialogue state tracking.
* Support spelling correction and WordNet synonym mapping.
* Detect and merge multiple intents.
* Establish a robust fallback and disclaimer framework.

---

### SLIDE 5: System Architecture
* **Frontend**: HTML5, CSS3, JS, Bootstrap 5.
* **Backend**: Flask routing API.
* **NLP Services**: Dual pipelines (`preprocess_classifier`, `preprocess_keywords`), entity parsers, and calculator engines.
* **Data Storage**: SQLite tables (`chat_history`, `session_profile`, `feedback`).

---

### SLIDE 6: Software & Hardware Specifications
* **Languages & OS**: Python 3.9+, macOS / Windows / Linux.
* **Core Libraries**: scikit-learn, NLTK, joblib, rapidfuzz.
* **Database**: SQLite 3.
* **Server Footprint**: runs efficiently on low-cost virtual private servers (1 vCPU, 1GB RAM) with zero API call costs.

---

### SLIDE 7: Use Case Diagram
* **Actors**: User and System Administrator.
* **Use Cases**:
  * Send Message & View History.
  * Trigger Fitness Calculations (BMI, BMR, Hydration).
  * Submit thumbs up/down rating feedback.
  * Switch/Manage Chat Sessions in sidebar.
  * Audit logs and trigger training.

---

### SLIDE 8: Data Flow Diagram (DFD Level 1)
* Detailed breakdown of data movement:
  * User Query $\rightarrow$ Spelling Check $\rightarrow$ Vocabulary Guard $\rightarrow$ Vectorizer $\rightarrow$ Logistic Regression $\rightarrow$ Keyword Boosts $\rightarrow$ SQLite Log $\rightarrow$ UI badges update $\rightarrow$ Chat bubble output.

---

### SLIDE 9: NLP Preprocessing Dual Pipeline
* **`preprocess_classifier()`**: Keep stopwords and avoid lemmatizing to preserve word orders for TF-IDF.
* **`preprocess_keywords()`**: Stopword removal, contraction expansion, WordNet lemmatizing, and synonym concept grouping.
* **Synonym Blacklist**: Prevents words like "mass" or "strength" from mapping to "bulk" or "muscle," avoiding collisions.

---

### SLIDE 10: Intent Classification (Statistical ML)
* **Vectorization**: TF-IDF using unigrams and bigrams, capturing phrases like "weight loss" or "muscle gain."
* **Classifier**: Multinomial Logistic Regression ($C=1.0$) using the Softmax function:
  $$P(Y = k \mid \mathbf{x}) = \frac{e^{\mathbf{w}_k^T \mathbf{x} + b_k}}{\sum_{j=1}^{K} e^{\mathbf{w}_j^T \mathbf{x} + b_j}}$$

---

### SLIDE 11: Hybrid Boosting & Multi-Intent Logic
* **Keyword Boosting**: Boosts probability score of classes by `+1.5` if key terms (e.g. "oats", "protein") are matched, bypassing unnecessary fallbacks.
* **Multi-Intent**: If secondary intents score $\ge 0.38$, returns a joint list and merges response templates dynamically.

---

### SLIDE 12: Dialogue State & Persistent Calculators
* **BMI**: Weight (kg) / Height (m)².
* **BMR (Mifflin-St Jeor)**:
  * Men: $10 \times \text{weight} + 6.25 \times \text{height} - 5 \times \text{age} + 5$
  * Women: $10 \times \text{weight} + 6.25 \times \text{height} - 5 \times \text{age} - 161$
* **Persistence**: Profile metrics upserted to SQLite database and synchronized as entity badges in UI.

---

### SLIDE 13: Database Design (ER Diagram)
* Three clean tables:
  * `chat_history`: stores sender, message, intent tag, confidence, and timestamp.
  * `session_profile`: holds height, weight, age, gender, goal, and update times.
  * `feedback`: logs thumbs up/down rating values associated with message IDs.

---

### SLIDE 14: System Testing & Pytest Logs
* **Pytest Unit Tests**: Passed 5 key integration suites (preprocessors, spelling corrections, session profiles, aliases, and follow-ups).
* **Robustness**: Bounded parameters prevent division by zero or server errors, displaying user-friendly validation warnings instead.

---

### SLIDE 15: Evaluation Metrics (Unseen Splits)
* Evaluated against a test dataset of 210 unseen queries:
  * **Clean English**: 85.71%
  * **Conversational English**: 80.00%
  * **Typographical Errors**: 68.57%
  * **Hinglish**: 65.71%
  * **Mixed Intents**: 57.14%
  * **Out-of-Scope Queries**: 91.43%
  * **Overall Accuracy**: **74.76%**

---

### SLIDE 16: Advantages & Applications
* Deterministic responses (no hallucinations or unsafe advice).
* CPU-only execution with sub-100ms response latency.
* **Applications**: Personal health companion, gym website assistants, corporate wellness portals.

---

### SLIDE 17: Conclusion & Future Scope
* **Conclusion**: Successfully built and validated an efficient, lightweight, context-aware chatbot for wellness guidance.
* **Future Scope**:
  * Connect with fitness wearable APIs (Fitbit, Apple Health).
  * Migrate database layer to cloud PostgreSQL.
  * Integrate Speech-to-Text for hands-free voice control.
