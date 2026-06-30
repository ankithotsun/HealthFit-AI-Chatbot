# 100 VIVA VOCE QUESTIONS & ANSWERS: HEALTHFIT AI

This document compiles **100 standard viva questions** and detailed answers to prepare for the final-year MCA project defense.

---

## Group 1: Project Overview & Architecture (Q1–15)

#### Q1: What is the title of your project?
**Answer**: The title is "HealthFit AI: An Intelligent Chatbot for Health and Fitness Guidance using Hybrid NLP Techniques."

#### Q2: What is the primary objective of HealthFit AI?
**Answer**: The objective is to provide personal health, fitness, and nutrition guidance through a real-time, context-aware chatbot interface using a hybrid machine learning classifier combined with persistent user profile tracking.

#### Q3: Why did you choose a hybrid NLP approach instead of a Large Language Model (LLM)?
**Answer**: LLMs are computationally heavy, require GPUs, generate high hosting costs, and are prone to hallucinations. HealthFit AI uses a local hybrid model (TF-IDF + Logistic Regression with keyword boosting) to ensure deterministic, medically safe responses, sub-100ms latency, and zero ongoing API costs.

#### Q4: Describe the architecture of your system.
**Answer**: The system follows a three-tier model:
1. *Presentation Layer*: Responsive HTML5, CSS3, JavaScript, and Bootstrap 5 dashboard.
2. *Application Layer*: Python Flask server handling routes, database CRUD, and NLP classification.
3. *Data Layer*: SQLite database (history, profiles, feedback) and joblib model files.

#### Q5: Who are the target users of this system?
**Answer**: Individuals seeking home or gym workouts, basic calorie calculations, water requirement suggestions, and nutritional values of common ingredients.

#### Q6: What is a hybrid chatbot?
**Answer**: A chatbot that combines statistical machine learning classifiers (like Logistic Regression) with rule-based models (like keyword boosting maps) to achieve higher accuracy.

#### Q7: How does the system handle complex user queries containing multiple questions?
**Answer**: Through a multi-intent detection module. If a secondary intent score is $\ge 0.38$, it returns a combined response merging templates from both intents.

#### Q8: What does "dialogue state tracking" mean in your project?
**Answer**: It refers to tracking and persisting user-supplied metrics (height, weight, age, gender, goal) across different conversational turns using an SQLite database.

#### Q9: How is the emergency disclaimer triggered?
**Answer**: If the user query contains clinical keywords like "chest pain" or "shortness of breath," the keyword booster assigns high priority to the `emergency_disclaimer` intent, prompting a medical warning.

#### Q10: How do administrators monitor the chatbot's performance?
**Answer**: Administrators can query the SQLite `feedback` table to review upvotes (👍) and downvotes (👎) mapped to user message histories.

#### Q11: What makes your chatbot "context-aware"?
**Answer**: It monitors the previous 3 user messages. If the current query is vague (e.g. *"explain it"*), it inherits the previous intent from the active chat history.

#### Q12: How does the chatbot scale dynamically for mobile devices?
**Answer**: By using Bootstrap 5's responsive grid system and responsive flex containers in the stylesheet.

#### Q13: What is the purpose of the sidebar in your UI?
**Answer**: It manages multiple chat sessions. Users can create new chats, switch between past conversations, or clear their current session history.

#### Q14: How does the server avoid crashes when users input negative parameters?
**Answer**: The calculator service verifies that inputs are within realistic bounds (e.g. height > 0, weight > 0) before executing calculations, returning a warning message if the input is invalid.

#### Q15: What is the role of `joblib` in your system?
**Answer**: Joblib is used to serialize (save) and deserialize (load) the fitted TF-IDF vectorizer and trained Logistic Regression model files.

---

## Group 2: Python & Flask Backend (Q16–30)

#### Q16: Why did you choose Flask over Django?
**Answer**: Flask is a lightweight micro-framework that provides only the core features needed for routing and request handling, keeping the system footprint small and ideal for local ML models. Django is much heavier and includes unnecessary built-in features (like an administrative panel) that we do not require.

#### Q17: Explain the file structure of your application.
**Answer**: The structure isolates responsibilities:
- `app.py`: Defines API routes.
- `controllers/`: Handles request parsing and coordinates services.
- `services/`: Contains metric calculators and formatting engines.
- `nlp/`: Preprocesses text and predicts intents.
- `utils/`: Manages SQLite transactions.

#### Q18: What routes are defined in your `app.py`?
**Answer**: 
- `POST /api/chat`: Process user queries.
- `POST /api/feedback`: Log upvotes/downvotes.
- `GET /api/history`: Retrieve session logs.
- `GET /`: Serves the UI page.

#### Q19: How do you parse JSON requests in Flask?
**Answer**: By calling `request.get_json()` in the route handler, which converts the incoming payload into a Python dictionary.

#### Q20: What is a virtual environment (venv)?
**Answer**: An isolated Python environment that lets you install project-specific packages without conflicting with the system-wide Python installation.

#### Q21: What is the purpose of `app.run()`?
**Answer**: It starts Flask's built-in development server, hosting the application locally on a default port (usually 5000).

#### Q22: How do you prevent Cross-Origin Resource Sharing (CORS) issues?
**Answer**: The frontend and backend run on the same origin (local host port 5000), which avoids cross-origin request issues.

#### Q23: How are exceptions handled in your API routes?
**Answer**: Routes are wrapped in `try-except` blocks. If an exception is raised, it is logged and returns a JSON error response with an HTTP 500 status.

#### Q24: What is the WSGI protocol?
**Answer**: Web Server Gateway Interface—a standard Python specification that enables web servers to communicate with web application frameworks like Flask.

#### Q25: How do you configure logging in Python?
**Answer**: By calling `logging.basicConfig(level=logging.INFO)`, which outputs diagnostic logs to the console for tracking and debugging.

#### Q26: What is a Flask Blueprint?
**Answer**: A way to organize a Flask application into distinct sub-modules. While not required for small apps, it helps structure larger codebases.

#### Q27: How does Flask serve static assets?
**Answer**: Files placed in the `static/` directory (like CSS styles or JS scripts) are served automatically by Flask's built-in static handler.

#### Q28: How do you retrieve query parameters from a GET request in Flask?
**Answer**: By accessing the `request.args` dictionary (e.g. `request.args.get('session_id')`).

#### Q29: What is `pip` in the Python ecosystem?
**Answer**: Pip is Python's package installer, used to download and manage third-party libraries from the Python Package Index (PyPI).

#### Q30: How does the backend prevent path traversal attacks when loading models?
**Answer**: Model file paths are constructed using absolute path anchors derived from `os.path.dirname(os.path.abspath(__file__))`, preventing path manipulation.

---

## Group 3: Database & SQLite (Q31–45)

#### Q31: Why did you choose SQLite over MySQL or MongoDB?
**Answer**: SQLite is a serverless, zero-configuration database that stores data in a single local file. This keeps the application self-contained and avoids the overhead of managing a separate database server.

#### Q32: What tables did you design for this system?
**Answer**: Three tables:
1. `chat_history`: Stores message logs.
2. `session_profile`: Stores user physical metrics.
3. `feedback`: Stores response ratings.

#### Q33: How does SQLite handle concurrent read/write operations?
**Answer**: SQLite locks the database file during writes. While not suitable for high-concurrency cloud environments, it is perfect for single-user or small-scale applications.

#### Q34: What is the primary key of the `session_profile` table?
**Answer**: The `session_id` (a UUID string representing the active session).

#### Q35: How does the system update existing user profiles without creating duplicate rows?
**Answer**: By executing an `INSERT OR REPLACE` query (or an upsert statement) matching the unique `session_id` primary key.

#### Q36: Why do you reverse the list of history records retrieved from `chat_history`?
**Answer**: The query fetches the most recent messages using `ORDER BY id DESC LIMIT 3` to get the latest context. We then reverse the results in Python to restore chronological order before merging.

#### Q37: How is the foreign key relationship designed in the `feedback` table?
**Answer**: The `message_id` column in the `feedback` table references the `id` column in the `chat_history` table using a `FOREIGN KEY` constraint with `ON DELETE CASCADE`.

#### Q38: What is an index in databases and did you use any?
**Answer**: An index improves query retrieval speeds. SQLite automatically creates indexes for primary keys (like `session_id`).

#### Q39: What is the purpose of `connection.commit()`?
**Answer**: It saves all pending changes made during a transaction to the database file.

#### Q40: How do you prevent SQL Injection attacks?
**Answer**: By using parameterized queries with placeholders (`?`) instead of string interpolation (like f-strings). The database driver safely sanitizes all parameters.

#### Q41: Explain the use of the `id INTEGER PRIMARY KEY AUTOINCREMENT` statement.
**Answer**: It defines an integer column that automatically increments by 1 for each new row, ensuring a unique ID for every record.

#### Q42: What is the benefit of setting `PRAGMA foreign_keys = ON`?
**Answer**: By default, SQLite does not enforce foreign key constraints. This command must be executed on connection start to enforce relational constraints.

#### Q43: How do you retrieve the last inserted row ID in SQLite?
**Answer**: By accessing `cursor.lastrowid` immediately after executing an insert query.

#### Q44: What database design normalization form did you follow?
**Answer**: The database follows Third Normal Form (3NF)—each table represents a single entity, and all columns depend strictly on the primary key.

#### Q45: How can the database be migrated to support high production scale in the future?
**Answer**: The database connection layer is modular, allowing you to swap out the SQLite driver for PostgreSQL without changing the core application logic.

---

## Group 4: Machine Learning & Classification (Q46–60)

#### Q46: What classifier did you implement?
**Answer**: A multinomial Logistic Regression classifier trained on TF-IDF features.

#### Q47: What features are fed into your classifier?
**Answer**: A numerical matrix generated by a TF-IDF vectorizer using unigrams and bigrams ($\text{ngram\_range}=(1, 2)$).

#### Q48: What is the validation accuracy of your retrained model?
**Answer**: The model achieved **97.65%** validation accuracy on the test split.

#### Q49: Explain the mathematical logic of Multinomial Logistic Regression.
**Answer**: It calculates the probability of each class using the Softmax function:
$$P(Y = k \mid \mathbf{x}) = \frac{e^{\mathbf{w}_k^T \mathbf{x} + b_k}}{\sum_{j=1}^{K} e^{\mathbf{w}_j^T \mathbf{x} + b_j}}$$
The class with the highest probability is predicted as the primary intent.

#### Q50: What is the purpose of the inverse regularization parameter $C$ in Logistic Regression?
**Answer**: $C$ controls the regularization strength. A smaller $C$ (e.g. 1.0) increases regularization, which helps prevent overfitting and reduces overconfidence on out-of-scope queries.

#### Q51: How does the system handle class imbalance?
**Answer**: The dataset compiler (`generate_intents.py`) enforces a balanced dataset of exactly 75 patterns for all 34 intents, ensuring uniform class representation.

#### Q52: What does TF-IDF stand for?
**Answer**: Term Frequency – Inverse Document Frequency.

#### Q53: Write the math equation for TF-IDF.
**Answer**:
$$\text{TF-IDF}(t, d, D) = TF(t, d) \times \log\left(\frac{1 + N}{1 + DF(t)}\right) + 1$$

#### Q54: Why are bigrams included in your TF-IDF vectorizer?
**Answer**: Bigrams (pairs of adjacent words) capture multi-word concepts like "weight loss" or "muscle gain" which have different meanings than their individual words.

#### Q55: What does `sublinear_tf=True` do in the vectorizer configuration?
**Answer**: It applies log normalization to the term frequency ($1 + \log(TF)$), which dampens the influence of highly repetitive words in a query.

#### Q56: How do you save the trained model to disk?
**Answer**: By calling `joblib.dump(model, model_path)`.

#### Q57: What is a classification report?
**Answer**: A performance summary showing Precision, Recall, F1-score, and Support metrics for each intent class.

#### Q58: Explain the difference between Precision and Recall.
**Answer**: 
* *Precision*: $\frac{TP}{TP + FP}$ — Out of all queries classified under an intent, how many were correct.
* *Recall*: $\frac{TP}{TP + FN}$ — Out of all actual queries for an intent, how many were correctly identified.

#### Q59: What is the F1-score?
**Answer**: The harmonic mean of Precision and Recall:
$$\text{F1} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

#### Q60: What is a Confusion Matrix?
**Answer**: A grid showing actual classes vs. predicted classes, helping to identify which intents are being confused by the classifier.

---

## Group 5: Natural Language Processing (NLP) & Text Preprocessing (Q61–75)

#### Q61: What is the difference between stemming and lemmatization?
**Answer**: Stemming chops off word endings using simple rules, which can produce non-words (e.g., "running" $\rightarrow$ "runn"). Lemmatization uses a dictionary and part-of-speech analysis to return the actual dictionary base form of a word (the lemma).

#### Q62: Why did you implement two separate preprocessing pipelines?
**Answer**: 
- `preprocess_classifier()` retains stopwords (e.g. "how", "are", "you") to preserve the natural sentence structure for TF-IDF intent classification.
- `preprocess_keywords()` strips stopwords and lemmatizes words to extract clean terms for keyword matching and entity extraction.

#### Q63: How are contractions expanded?
**Answer**: Using a compiled regular expression lookup map that converts contractions (e.g., *"i'm"*, *"can't"*) into standard forms (e.g., *"i am"*, *"cannot"*).

#### Q64: Why are negation terms like "not" or "no" preserved during stopword removal?
**Answer**: Removing negations changes the meaning of a query (e.g., *"not tired"* becomes *"tired"*), which would cause the classifier to return the wrong intent.

#### Q65: What is WordNet?
**Answer**: WordNet is a large lexical database of English words grouped into sets of cognitive synonyms (synsets).

#### Q66: How is WordNet synonym mapping used in your preprocessor?
**Answer**: It maps related words to a set of core fitness concepts. For example, if a query contains "obese" or "flab", it maps them to the concept "fat" for classification.

#### Q67: Why did you create a synonym expansion blacklist?
**Answer**: To prevent common words like "mass" or "strength" from undergoing synonym expansion, which would cause intent classification collisions (e.g. mapping "Body Mass Index" to "bulk").

#### Q68: How does the spelling correction layer work?
**Answer**: It uses a target dictionary for exact matches, and applies **RapidFuzz** to calculate Levenshtein distance for misspelled words, correcting them if similarity $\ge 90\%$.

#### Q69: Explain Levenshtein Distance.
**Answer**: The minimum number of single-character edits (insertions, deletions, or substitutions) required to change one word into another.

#### Q70: What is tokenization?
**Answer**: The process of splitting a continuous string of text into individual units (tokens), such as words or punctuation marks.

#### Q71: How does punctuation removal prevent word merging?
**Answer**: By replacing punctuation marks with spaces before collapsing multiple spaces into a single space, preventing adjacent words from being merged.

#### Q72: What NLTK corpora did your system download?
**Answer**: `punkt` (tokenizer), `stopwords` (stopword lists), and `wordnet` / `omw-1.4` (synonym databases).

#### Q73: How does the system detect Hinglish inputs?
**Answer**: By including common Romanized Hindi terms (e.g., *"kam kare"*, *"nashta"*) in the training patterns, allowing the classifier to map them to the correct intents.

#### Q74: Why is lowercase conversion important in NLP?
**Answer**: It normalizes the text so that words like "Protein", "PROTEIN", and "protein" are treated as the same token.

#### Q75: How does the preprocessor handle numbers?
**Answer**: It preserves numbers because they contain important parameters for health calculations (e.g. *"I weigh 80 kg"*).

---

## Group 6: Dialog State Tracking & System Logic (Q76–90)

#### Q76: How does the chatbot extract physical metrics like height and weight?
**Answer**: By using regular expressions to match numbers followed by units (e.g., `cm`, `kg`, `lbs`, `inches`) in `entity_extractor.py`.

#### Q77: What formula is used to calculate BMI?
**Answer**:
$$\text{BMI} = \frac{\text{Weight in Kilograms}}{(\text{Height in Meters})^2}$$

#### Q78: Detail the BMI weight categories used in your system.
**Answer**:
* $< 18.5$: Underweight
* $18.5 - 24.9$: Normal Weight
* $25.0 - 29.9$: Overweight
* $\ge 30.0$: Obese

#### Q79: How does the chatbot calculate BMR for men?
**Answer**: Using the Mifflin-St Jeor equation:
$$\text{BMR} = 10 \times \text{Weight (kg)} + 6.25 \times \text{Height (cm)} - 5 \times \text{Age (years)} + 5$$

#### Q80: How does the BMR formula change for women?
**Answer**: The constant term changes from $+5$ to $-161$:
$$\text{BMR} = 10 \times \text{Weight (kg)} + 6.25 \times \text{Height (cm)} - 5 \times \text{Age (years)} - 161$$

#### Q81: What is the Mifflin-St Jeor equation?
**Answer**: A widely accepted clinical formula used to estimate an individual's Basal Metabolic Rate (BMR) based on their physical metrics.

#### Q82: How does the chatbot estimate daily water requirements?
**Answer**: It calculates the target based on the user's weight:
$$\text{Water (Liters)} = \text{Weight (kg)} \times 0.035$$
For an 80kg user, the recommended target is 2.8 liters per day.

#### Q83: Where are calculations handled in the codebase?
**Answer**: In the helper functions inside `services/nlp_service.py`.

#### Q84: How are response templates customized with user metrics?
**Answer**: The templates contain placeholders (e.g. `{bmi_score}`, `{water_target}`) that are dynamically replaced with calculated values before returning the response.

#### Q85: What happens to placeholders if the user hasn't provided their metrics?
**Answer**: A regex cleaner strips any unresolved placeholders from the response template, replacing them with helpful tips instead.

#### Q86: How does the system prevent out-of-scope queries from triggering random intents?
**Answer**: If a query has zero vocabulary overlap with the classifier's training patterns, the system automatically redirects the query to the fallback handler.

#### Q87: Explain the fallback handling logic.
**Answer**: Instead of returning a generic error, the fallback handler returns a guided menu prompting the user to select from supported topics (Workouts, Nutrition, calculations).

#### Q88: How does follow-up inheritance work for short messages?
**Answer**: If the user types a short follow-up phrase (e.g. *"why?"*), the system bypasses classification and inherits the previous intent from the active session history.

#### Q89: How does the system handle intent aliases?
**Answer**: It maintains an alias map (e.g. mapping "fat" to `workout_weight_loss`). If the user input matches an alias, it skips classification and routes directly to that intent.

#### Q90: How does the chatbot handle mixed-intent queries (e.g. *"suggest a diet and squats guide"*)?
**Answer**: It matches the multiple intents, retrieves the response templates for each, and joins them using a transition paragraph:
```
"I noticed you are asking about multiple topics! Here is some personalized advice on both:"
```

---

## Group 7: Testing, Performance & Software Engineering (Q91–100)

#### Q91: What testing methodology did you use?
**Answer**: We used automated unit testing with `pytest` for core functions, and system-level evaluation scripts to test the model against unseen query splits.

#### Q92: What test splits were used in your evaluation?
**Answer**: Six splits: Clean English, Conversational English, Typographical Errors, Hinglish, Mixed Intents, and Out-of-Scope Queries.

#### Q93: What was the overall accuracy across these evaluation splits?
**Answer**: The system achieved an overall accuracy of **74.76%** (157 out of 210 queries correct).

#### Q94: How does the system prevent division by zero in calculations?
**Answer**: The calculation helpers verify that height and weight values are greater than zero before performing calculations.

#### Q95: What is the average response latency of your application?
**Answer**: Local round-trip API latency is under 10 milliseconds, and network latency is under 100 milliseconds.

#### Q96: How did you implement automated tests for session memory?
**Answer**: The test runner spins up a temporary SQLite database, sends a message containing weight metrics, sends a follow-up query, and asserts that the weight metric is preserved and referenced in the response.

#### Q97: What version control practices did you follow?
**Answer**: We used Git to manage code changes, committing changes incrementally as features were completed.

#### Q98: How does the system secure user session identifiers?
**Answer**: Session IDs are generated as secure UUIDs on the client side and stored in browser `localStorage`, preventing session prediction.

#### Q99: Why is standardizing software requirements (SRS) important in engineering?
**Answer**: An SRS establishes clear expectations, constraints, and metrics, ensuring the development team aligns with the project goals.

#### Q100: What is the future scope of HealthFit AI?
**Answer**: Future enhancements include integrating user authentication (Firebase Auth), connecting to fitness wearables (Google Fit/Apple Health), and adding a voice-guided assistant.
