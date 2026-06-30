# CHAPTER 14: FEASIBILITY STUDY

Before initiating coding, a feasibility study was conducted to evaluate the technical, operational, and economic viability of **HealthFit AI**.

## 14.1 Technical Feasibility

The technical feasibility analyzes whether the development organization has the technology, libraries, and processing hardware required to build and run the chatbot.
- **Python Ecosystem**: The Python programming language is highly suited for this project. It offers standard libraries for numerical calculations and mature machine learning libraries like `scikit-learn` and `NLTK`.
- **Stateless/Lightweight CPU Execution**: The chosen classification pipeline (TF-IDF + Logistic Regression) is computationally extremely light. It does not require dedicated GPUs or cloud tensor processors. Model inference takes less than 5 milliseconds on a single-core CPU, making it highly feasible to host on low-cost virtual private servers (VPS).
- **SQLite DB Management**: Since database requirements are limited to session metrics, chat logs, and feedback entries, SQLite is a perfect fit. It is serverless, requires zero configuration, stores data in a single local file, and provides fast read/write speeds.
- **Web Standards compatibility**: The frontend uses standard HTML5, CSS3, and ES6 JavaScript. These are universally supported by all modern web browsers (Chrome, Safari, Firefox, Edge) without requiring complex plugins or node builds.

Therefore, the project is **highly technically feasible**.

## 14.2 Operational Feasibility

Operational feasibility evaluates how well the proposed system solves the users' problems and how easily it can be integrated into their daily routines.
- **Intuitive User Interface**: The UI is designed like a standard modern messaging app (similar to WhatsApp or Telegram). Users do not need any training to use it—they simply type queries in the chat input and press Enter.
- **Visual Profiling (Badges)**: The dynamic UI updates physical metric badges in real-time. This keeps users informed of what stats the bot is currently using to personalize their calorie or water recommendations.
- **Administrative Audits**: The database logs feedback ratings (upvotes and downvotes). This allows the system administrator to query failures easily, adjust training patterns, and retrain the model, maintaining high operational relevance.

Therefore, the project is **highly operationally feasible**.

## 14.3 Economic Feasibility

Economic feasibility determines if the financial benefits of the system justify the development and hosting costs.
- **Development Cost**: The project is built entirely on open-source software (Python, Flask, scikit-learn, NLTK, Bootstrap). There are no commercial software licensing fees or proprietary software dependencies.
- **Zero API Call Costs**: Unlike LLM-based chatbots (which charge per token on APIs like OpenAI or Google Gemini), HealthFit AI runs its machine learning classification and keyword boosting locally. There are no ongoing query processing costs.
- **Low Hosting Overhead**: Due to the lightweight nature of Flask and the statistical classifier, the server footprint is negligible. It can be hosted on a standard $5/month cloud VPS, making it highly cost-effective.

Therefore, the project is **highly economically feasible**.
