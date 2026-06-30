# CHAPTER 10: SCOPE

## 10.1 Functional Scope

The functional scope of **HealthFit AI** defines the precise capabilities and operations of the system. It is structured around the following core areas:

1. **Fitness Calculations**:
   - **Body Mass Index (BMI)**: Performs calculations using height (cm/inches) and weight (kg/lbs) to output the score and weight classification (Underweight, Normal, Overweight, Obese) along with specific advice.
   - **Basal Metabolic Rate (BMR) & Daily Calories**: Estimates the daily energy expenditure based on height, weight, age, and gender using the Mifflin-St Jeor equation.
   - **Hydration Target**: Determines target daily water intake (liters) dynamically adjusted by the user's weight.

2. **Nutritional Guidance**:
   - Provides food suggestions divided by meals: `healthy_breakfast`, `healthy_lunch`, `healthy_dinner`, and `healthy_snacks`.
   - Offers ingredient-specific macros and guidance for core foods such as oatmeal (`healthy_carb_sources`), eggs/chicken breast (`healthy_protein_foods`), avocado/nuts (`healthy_fat_sources`), and broccoli/spinach/yogurt (`healthy_greens`).
   - Advises on structured dietary paths (`dietary_patterns`) such as Vegan, Vegetarian, Ketogenic, and Intermittent Fasting.

3. **Workout and Physical Training Programs**:
   - Structured routines for `workout_beginner`, `workout_weight_loss` (fat burning), and `workout_muscle_gain` (hypertrophy).
   - Exercise-specific forms and tips for core exercises: pushups/planks/pullups (`body_weight_exercises`), squats/lunges (`leg_exercises`), bicep curls (`arm_exercises`), and crunches (`abdominal_exercises`).
   - Flexibility, mobility, and cool-down techniques (`yoga_stretching`), and endurance-focused advice (`cardio_workout`).

4. **Conversational Support**:
   - Handling social cues (`greeting`, `goodbye`, `thanks`, `help`, `bot_identity`).
   - Continuous chat history preservation and message history management via a sidebar dashboard.
   - Dynamic user profile state visualization (badges indicating active height/weight/goal).

## 10.2 Technical Boundaries

While HealthFit AI is highly capable within its domain, it is essential to outline its technical boundaries:
- **No Generative Advice**: The system does not generate unstructured free-form text dynamically (unlike LLMs). All advice is composed from structured templates, avoiding "hallucinations" or unsafe medical recommendations.
- **No Medical Diagnosis**: The chatbot is strictly an informational tool. It does not prescribe medications, diagnose pathological conditions, or recommend clinical treatments. In case of emergency inputs, it immediately routes to the `emergency_disclaimer` tag.
- **Local SQLite Persistence**: Session memory is stored in a local SQLite file database. It does not synchronize profiles across multiple client devices or cloud-based server endpoints in its current configuration.
- **Unsupervised Training**: The statistical classification model is trained offline. It does not update its machine learning weights (TF-IDF vectorizer and Logistic Regression coefficients) dynamically in real-time based on conversations. Retraining must be triggered via `train_model.py`.
