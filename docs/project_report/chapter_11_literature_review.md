# CHAPTER 11: LITERATURE REVIEW

## 11.1 Review of Existing Systems

To establish the context of the proposed **HealthFit AI** system, it is vital to review existing digital health and fitness solutions, identifying their strengths and functional limitations.

### 1. Diet and Calorie Tracking Applications (e.g., MyFitnessPal, Lose It!)
- **Strengths**: These platforms offer massive databases of food items, allowing users to log calorie intake and track daily macros. They also include BMR/TDEE calculators to set daily calorie targets.
- **Weaknesses**: They rely entirely on manual inputs and rigid, form-based interfaces. If a user has a question like, *"What are some high-protein breakfast options?"*, they cannot ask the application directly. Instead, they must browse blogs or manually search food databases. There is no conversational guidance or real-time dialogue assistant.

### 2. General-Purpose Search Engines (e.g., Google, Bing)
- **Strengths**: Provide access to millions of fitness articles, exercise videos, and diet templates.
- **Weaknesses**: Search results are highly generalized and often contain conflicting advice. A user searching for a workout plan will face information overload, with different websites recommending differing splits (e.g., full body vs. push-pull-legs). Furthermore, search engines do not remember user metrics (height, weight), preventing personalization of advice.

### 3. Rule-Based Chatbots (e.g., Early-generation Messenger bots)
- **Strengths**: Simple to build, computationally cheap, and highly deterministic.
- **Weaknesses**: These systems rely on rigid decision trees, button menus, or regular expression matching. If a user types a sentence that varies slightly from the predefined rules, the chatbot fails and displays generic error messages like, *"I did not understand that."* They lack the ability to comprehend natural sentence structures, handle spelling errors, or manage conversational context.

## 11.2 Traditional vs. Modern NLP Techniques

The field of Natural Language Processing has evolved significantly, progressing from strict rule-based syntax checking to advanced deep learning architectures. Understanding these differences justifies the hybrid machine learning architecture chosen for HealthFit AI.

| NLP Technique | Description | Advantages | Disadvantages |
| :--- | :--- | :--- | :--- |
| **Rule-Based & Regex** | Employs hardcoded rules and pattern matching to trigger responses. | Fast, deterministic, requires zero training data. | Extremely rigid, fails on typos, synonyms, or variations. |
| **Statistical Machine Learning** | Uses TF-IDF for numerical feature extraction and classifiers like Logistic Regression or SVMs. | High classification accuracy, handles sentence variations, lightweight (<10MB), fast CPU execution. | Requires training data, cannot generate creative/unseen text, relies on static parameters. |
| **Large Language Models (LLMs)** | Generative models (e.g., GPT, Gemini) built on the Transformer architecture. | Highly conversational, generates human-like text, understands complex context. | High latency, expensive API costs, requires GPUs, prone to hallucinations (unsafe medical advice). |

### Selection Rationale for HealthFit AI
HealthFit AI implements a **Hybrid NLP Engine** that combines statistical machine learning (TF-IDF + Logistic Regression) with domain-specific keyword boosting, fuzzy matching (RapidFuzz), and WordNet synonym expansion. This hybrid approach:
1. **Ensures Determinism**: Using structured templates guarantees the chatbot never generates hallucinated or medically unsafe advice.
2. **Maintains Low Overhead**: The entire classification pipeline operates on the host CPU in milliseconds, bypassing expensive API subscriptions or heavy deep learning frameworks.
3. **Handles Real-World Input**: WordNet synonym mapping resolves colloquial variations (e.g., "corpulence" or "flab" mapping to the concept "fat"), while RapidFuzz manages typographical spelling mistakes.
