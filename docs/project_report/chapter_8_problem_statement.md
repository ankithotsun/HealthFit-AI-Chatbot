# CHAPTER 8: PROBLEM STATEMENT

## 8.1 Current Market Challenges

Despite the abundance of fitness applications, wearables, and online diet planners, users continue to face significant challenges in acquiring accurate and customized health guidance. The primary challenges in the current market include:
1. **Information Overload**: A search for "weight loss diet" yields millions of pages containing contradictory suggestions (e.g., low-carb vs. low-fat), which confuses users and leads to ineffective results.
2. **Lack of Personalization**: Most free calculators or resources do not remember the user's details. If a user calculates their BMI, they must re-enter their physical metrics on subsequent visits or pages.
3. **Rigid Interface Interactions**: Existing health chatbots rely on rigid menu buttons or static command-line interfaces. They are unable to parse complex sentences or identify multiple intents (e.g., "I want a beginner gym plan and a high-protein breakfast suggestion") in a single input.
4. **Poor Handling of Typographical and Lexical Variations**: Users do not always type grammatically clean queries. A typo like "protin rich diet" or a Romanized Hindi phrase (Hinglish) like "pet ki charbi kaise kam kare" is usually ignored or misclassified as out-of-scope by traditional pattern-matching engines.
5. **High Computational Overhead of LLMs**: While generative AI models (like GPT or Gemini) are highly conversational, deploying them for simple classification and calculator operations is expensive, suffers from latency issues, and risks "hallucinations" where the bot might generate unsafe medical advice.

## 8.2 Need for the Proposed System

To mitigate these challenges, there is a clear need for a specialized, lightweight, and hybrid health chatbot that acts as a bridge. The proposed **HealthFit AI** chatbot addresses this gap by:
- Operating locally with statistical machine learning and rule-based layers, ensuring instantaneous response latencies and zero API call costs.
- Integrating a spelling correction layer (RapidFuzz) and a synonym normalization lexicon (WordNet) to handle colloquial conversational variations and typos.
- Retaining session profiles (weight, height, age, gender, goal) in a lightweight SQLite database so that users do not have to re-enter their stats, enabling the bot to reference their BMI or daily calorie budgets dynamically in conversations.
- Designing a multi-intent detector that identifies overlapping concepts and merges responses gracefully.
- Providing specific, guided fallback suggestions when queries are out-of-scope, steering the user back to valid health and exercise domains.
