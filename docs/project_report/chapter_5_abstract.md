# ABSTRACT

In the modern digital era, maintaining optimal health and fitness has become a significant challenge due to sedentary lifestyles, poor dietary habits, and the lack of personalized, accessible guidance. Traditional health consulting is often expensive and time-consuming, while generic search engines fail to provide structured, interactive advice. To address this, this project presents **HealthFit AI**, an intelligent, interactive chatbot designed to provide real-time, context-aware health and fitness guidance using a hybrid Natural Language Processing (NLP) engine.

The core architecture of HealthFit AI consists of a robust Python and Flask-based backend integrated with a lightweight frontend using HTML5, Bootstrap 5, and vanilla JavaScript. Unlike standard chatbots that rely on single-intent classification, HealthFit AI features a hybrid NLP pipeline combining Statistical Machine Learning (TF-IDF + Logistic Regression) with domain-specific keyword boosting and WordNet synonym expansion. This combination achieves high intent classification accuracy (97.65% validation accuracy) on a custom dataset of 34 intents and 2,550 balanced patterns, including Hinglish (Romanized Hindi) and typographical errors.

Key features include:
1. **Multi-Intent Detection**: Identifying complex queries containing multiple topics (e.g., "lose weight and build muscle") and dynamically merging response templates.
2. **Dialogue State & Session Memory**: Automatically tracking and persisting user physical metrics (height, weight, age, gender, and goals) across requests in an SQLite database, enabling personalized calculations (BMI, BMR, daily calories, and hydration).
3. **Conversational Follow-up Resolution**: Utilizing sliding history context to resolve vague queries (e.g., "explain it", "tell me more") by inheriting previous intents.
4. **Fuzzy Spelling Correction**: Utilizing RapidFuzz (similarity $\ge 90\%$) to correct common typographical errors before processing.

The system is tested comprehensively under real-world scenarios, demonstrating excellent stability, fast response latencies (<100ms), and high conversational relevance, offering a scalable, low-overhead solution for personal wellness assistance.

**Keywords**: *Natural Language Processing, Chatbot, Health and Fitness, Machine Learning, Hybrid Classifier, Logistic Regression, WordNet, Dialogue State Tracking, Flask, SQLite.*
