# CHAPTER 9: OBJECTIVES

The implementation of **HealthFit AI** is driven by a structured set of goals categorized into primary system objectives and secondary operational objectives.

## 9.1 Primary Objectives

1. **Robust Intent Classification**: 
   Develop an NLP engine capable of mapping user messages to 34 fitness-related intents (such as `workout_weight_loss`, `healthy_breakfast`, `hydration`, `bmi`) with a validation accuracy of over 95%.
2. **Context-Aware Dialogue State Management**:
   Maintain a persistent user profile (SQLite-backed) for session tracking. If a user states, *"I weigh 80 kg and my height is 180 cm,"* the chatbot must automatically calculate and store their BMI, then reuse these stats in future queries (e.g., estimating daily water targets or BMR).
3. **Multi-Intent Parse Execution**:
   Provide a parser that can identify when a user is asking about multiple wellness topics simultaneously (e.g., *"suggest a diet and a squat workout"*). It must extract both intents (`healthy_lunch` + `leg_exercises`) and merge the dynamic responses.
4. **Resilient Conversational Pipeline**:
   Integrate spelling correction (RapidFuzz $\ge 90\%$) and WordNet synonym mapping to clean, expand, and route inputs correctly, even when they contain grammatical slip-ups or Hinglish terms.
5. **Out-of-Scope Fallback Filtering**:
   Establish a strict vocabulary guard that detects completely unrelated queries (e.g., *"who is the president"* or *"weather updates"*) and responds with helpful options to redirect the conversation.

## 9.2 Secondary Objectives

1. **User Interface Accessibility**:
   Design a mobile-responsive chat dashboard featuring typing animations, auto-scroll, message timestamps, dynamic entity badges, and upvote/downvote feedback loops.
2. **Fast Response Latencies**:
   Optimize text preprocessing and vectorization pipelines to ensure round-trip API latencies are below 100 milliseconds, ensuring smooth, real-time user engagement.
3. **Historical Logs and Auditing**:
   Persist all chat transcripts and user feedback in an SQLite database, allowing administrators to audit chatbot decisions, identify common failure cases, and track user satisfaction metrics.
4. **Domain Security & Disclaimers**:
   Integrate an emergency disclaimer module that immediately flags medical-related keywords (e.g., *"chest pain"*, *"breathing difficulties"*) and prompts the user to seek professional clinical assistance.
