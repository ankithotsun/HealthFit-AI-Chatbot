# CHAPTER 24: LIMITATIONS

While **HealthFit AI** is a highly efficient and context-aware chatbot within its scope, it is important to identify its current technical and operational limitations.

## 24.1 Technical Limitations

1. **Closed Domain Boundary**:
   The chatbot is strictly limited to health and fitness topics. Its classification engine is bounded by 34 core intents. If a user asks a question outside this domain (e.g. *"how to write a Python script"*), the system cannot provide a useful response and will default to the fallback route.
2. **Offline Knowledge Base**:
   The bot's responses are generated from predefined templates. It does not fetch real-time web content. For example, it cannot check current local gym locations or retrieve updated nutrition databases from online repositories.
3. **No Semantic Deep-Learning Representation**:
   While TF-IDF + Logistic Regression is highly efficient, it relies on n-gram match profiles and term frequencies. It lacks the deep semantic word embeddings (such as Word2Vec, BERT, or transformers) needed to understand complex metaphors or indirect phrasing.
4. **Single-Instance Database (SQLite)**:
   SQLite is file-backed and does not support high-concurrency write operations. If deployed to a large production environment with thousands of concurrent users writing to `chat_history` and `feedback` simultaneously, database locks and transaction bottlenecks may occur.

## 24.2 Operational Limitations

1. **Limited Multi-Intent Context Handling**:
   While the system successfully identifies joint intents (e.g., combining a diet query and an exercise query), it only merges their templates. It cannot synthesize a single, unified response (e.g., creating a highly customized calorie-matching meal plan based on specific lifts).
2. **Language Constraints**:
   The spelling corrector (RapidFuzz) and WordNet synonym mapping are designed for English vocabulary. While Hinglish queries are classified using training patterns, the spelling check and WordNet normalization layers do not support Romanized Hindi translation or Hindi script (Devanagari).
3. **Absence of User Authentication**:
   The current implementation tracks sessions using browser-generated UUIDs stored in `localStorage`. There is no login or user authentication mechanism. If a user clears their browser cache, their session history and physical profile badges are reset.
