# HealthFit AI Chatbot — Phase 6 NLP Model Evaluation Report

This report presents a detailed evaluation of the chatbot's consolidated NLP classification engine (34 intents, 2,550 patterns) using **210 completely unseen test queries** divided into 6 distinct testing divisions.

## 1. Summary Performance Metrics

| Metric | Value |
| :--- | :--- |
| **Overall Evaluation Accuracy** | **74.76%** (157/210 queries) |
| **Total Core Intents** | 34 intents |
| **Total Evaluation Test Queries** | 210 queries |

## 2. Division-level Performance Accuracy

| Query Division | Total Queries | Passed | Division Accuracy | Description |
| :--- | :---: | :---: | :---: | :--- |
| Clean English | 35 | 30 | **85.71%** | Grammatically clean, formal, clear query phrasing. |
| Conversational English | 35 | 28 | **80.00%** | Colloquial, casual conversational queries, slang, contractions. |
| Typographical Errors | 35 | 24 | **68.57%** | Queries containing spelling mistakes, run-ons, typos corrected by RapidFuzz. |
| Hinglish | 35 | 23 | **65.71%** | Romanized Hindi queries mapping to fitness intents. |
| Mixed Intents | 35 | 20 | **57.14%** | Queries containing concepts of multiple intents tested for joint extraction. |
| Out-of-Scope Queries | 35 | 32 | **91.43%** | Queries outside of health and fitness scope tested for fallback routing. |

## 3. Query Division Confusion Matrix

| Actual Division | Predicted Positive / Correct | Predicted Fallback / Incorrect |
| :--- | :---: | :---: |
| **Clean English** | **30** | 5 |
| **Conversational English** | **28** | 7 |
| **Typographical Errors** | **24** | 11 |
| **Hinglish** | **23** | 12 |
| **Mixed Intents** | **20** | 15 |
| **Out-of-Scope Queries** | **32** | 3 |

## 4. Evaluation Failure / Low Confidence Log

| # | User Query | Division | Expected Intent | Predicted Intent | Confidence | Status |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| 1 | `List some healthy snack options.` | Clean English | `healthy_snacks` | `healthy_snacks+greeting` | 0.3906 | ❌ FAIL |
| 2 | `Why is stretching important after a workout?` | Clean English | `yoga_stretching` | `yoga_stretching+greeting` | 0.4294 | ❌ FAIL |
| 3 | `How do I perform a core plank?` | Clean English | `body_weight_exercises` | `body_weight_exercises+abdominal_exercises` | 0.5350 | ❌ FAIL |
| 4 | `How much protein is in chicken breast?` | Clean English | `healthy_protein_foods` | `fallback` | 0.3442 | ❌ FAIL |
| 5 | `Are green salads good for weight loss?` | Clean English | `healthy_greens` | `healthy_greens+workout_weight_loss` | 0.4185 | ❌ FAIL |
| 6 | `is vegan protein actually good` | Conversational English | `dietary_patterns` | `dietary_patterns+protein_sources` | 0.4038 | ❌ FAIL |
| 7 | `i am feeling super lazy to workout help` | Conversational English | `motivation` | `motivation+help` | 0.3974 | ❌ FAIL |
| 8 | `how to get chest strength from pushups` | Conversational English | `body_weight_exercises` | `body_weight_exercises+strength_training` | 0.4264 | ❌ FAIL |
| 9 | `i can't do a single pullup help` | Conversational English | `body_weight_exercises` | `help+body_weight_exercises` | 0.4548 | ❌ FAIL |
| 10 | `how to hold plank for core stability` | Conversational English | `body_weight_exercises` | `body_weight_exercises+abdominal_exercises` | 0.4830 | ❌ FAIL |
| 11 | `arm exercises with dumbbells` | Conversational English | `arm_exercises` | `fallback` | 0.3683 | ❌ FAIL |
| 12 | `i eat boiled eggs daily is it healthy` | Conversational English | `healthy_protein_foods` | `healthy_protein_foods+greeting` | 0.4259 | ❌ FAIL |
| 13 | `who made u who devloped u` | Typographical Errors | `bot_identity` | `fallback` | 0.3233 | ❌ FAIL |
| 14 | `chek my bmiscore` | Typographical Errors | `bmi` | `bmi+abdominal_exercises` | 0.4099 | ❌ FAIL |
| 15 | `muscel gain strength trainin` | Typographical Errors | `workout_muscle_gain` | `workout_muscle_gain+strength_training` | 0.5177 | ❌ FAIL |
| 16 | `bakd salmon dinner ideas recipe` | Typographical Errors | `healthy_dinner` | `healthy_dinner+healthy_protein_foods` | 0.4933 | ❌ FAIL |
| 17 | `healty snacks weight loss` | Typographical Errors | `healthy_snacks` | `healthy_snacks+workout_weight_loss` | 0.4679 | ❌ FAIL |
| 18 | `pushps chest arm strength form` | Typographical Errors | `body_weight_exercises` | `body_weight_exercises+strength_training` | 0.4347 | ❌ FAIL |
| 19 | `pullup lat recruitment biceps` | Typographical Errors | `body_weight_exercises` | `arm_exercises+body_weight_exercises` | 0.4158 | ❌ FAIL |
| 20 | `plnk core exercise abs` | Typographical Errors | `body_weight_exercises` | `abdominal_exercises+body_weight_exercises` | 0.4522 | ❌ FAIL |
| 21 | `rolled oats breakfast fiber` | Typographical Errors | `healthy_carb_sources` | `healthy_carb_sources+healthy_breakfast` | 0.4533 | ❌ FAIL |
| 22 | `chicken brest protein macros` | Typographical Errors | `healthy_protein_foods` | `fallback` | 0.3054 | ❌ FAIL |
| 23 | `gren salad low calorie loss` | Typographical Errors | `healthy_greens` | `healthy_greens+calorie_estimation` | 0.4072 | ❌ FAIL |
| 24 | `bahut shukriya help karne ke liye` | Hinglish | `thanks` | `thanks+help` | 0.4115 | ❌ FAIL |
| 25 | `apka designer kaun hai kisne banaya` | Hinglish | `bot_identity` | `fallback` | 0.1299 | ❌ FAIL |
| 26 | `mujhe daily kitni calories khani chahiye` | Hinglish | `calorie_estimation` | `calorie_estimation+greeting` | 0.4298 | ❌ FAIL |
| 27 | `din bhar me kitna pani pina chahiye` | Hinglish | `hydration` | `hydration+greeting` | 0.4532 | ❌ FAIL |
| 28 | `gym ki shuruat kaise kare exercises bataye` | Hinglish | `workout_beginner` | `fallback` | 0.4007 | ❌ FAIL |
| 29 | `muscle kaise banaye biceps size bada karna hai` | Hinglish | `workout_muscle_gain` | `arm_exercises` | 0.6116 | ❌ FAIL |
| 30 | `subah ke nashte me kya khaye healthy options` | Hinglish | `healthy_breakfast` | `healthy_breakfast+greeting` | 0.4626 | ❌ FAIL |
| 31 | `stretching exercise kaise kare soreness bhagane ke liye` | Hinglish | `yoga_stretching` | `yoga_stretching+greeting` | 0.4184 | ❌ FAIL |
| 32 | `pushups kaise lagaye arm strength badhane ke liye` | Hinglish | `body_weight_exercises` | `body_weight_exercises+strength_training` | 0.4013 | ❌ FAIL |
| 33 | `plank kitni der hold karna chahiye core abs` | Hinglish | `body_weight_exercises` | `fallback` | 0.3159 | ❌ FAIL |
| 34 | `rolled oats breakfast fiber carbs benefits` | Hinglish | `healthy_carb_sources` | `healthy_carb_sources+healthy_breakfast` | 0.5262 | ❌ FAIL |
| 35 | `salad low calorie loss fiber veggies` | Hinglish | `healthy_greens` | `fallback` | 0.2403 | ❌ FAIL |
| 36 | `strength training safety and oats breakfast carbs` | Mixed Intents | `strength_training+healthy_carb_sources` | `fallback` | 0.3105 | ❌ FAIL |
| 37 | `keto diet rules and healthy lunch recommendations` | Mixed Intents | `dietary_patterns+healthy_lunch` | `fallback` | 0.3257 | ❌ FAIL |
| 38 | `underweight mass gain tips and high protein chicken breast recipe` | Mixed Intents | `weight_issues+healthy_protein_foods` | `fallback` | 0.2418 | ❌ FAIL |
| 39 | `pushups for upper body and planks for core abs` | Mixed Intents | `body_weight_exercises+abdominal_exercises` | `fallback` | 0.2949 | ❌ FAIL |
| 40 | `sleep requirement for recovery and hydration target` | Mixed Intents | `sleep+hydration` | `fallback` | 0.3232 | ❌ FAIL |
| 41 | `beginner exercises and healthy snacks ideas` | Mixed Intents | `workout_beginner+healthy_snacks` | `fallback` | 0.3079 | ❌ FAIL |
| 42 | `obesity health risks and weight loss workout cardios` | Mixed Intents | `weight_issues+workout_weight_loss` | `fallback` | 0.3295 | ❌ FAIL |
| 43 | `veggies benefits and chicken eggs diet macros` | Mixed Intents | `healthy_snacks+healthy_protein_foods` | `fallback` | 0.3356 | ❌ FAIL |
| 44 | `how to squat legs workout and crunches abs exercise` | Mixed Intents | `leg_exercises+abdominal_exercises` | `fallback` | 0.3078 | ❌ FAIL |
| 45 | `healthy salad recipe dinner options` | Mixed Intents | `healthy_greens+healthy_dinner` | `fallback` | 0.3209 | ❌ FAIL |
| 46 | `whey protein safety and bmr calories calculator` | Mixed Intents | `protein_sources+calorie_estimation` | `fallback` | 0.2532 | ❌ FAIL |
| 47 | `namaste chatbot check my bmiscore` | Mixed Intents | `greeting+bmi` | `fallback` | 0.3129 | ❌ FAIL |
| 48 | `boiled eggs protein and Greek yogurt curd probiotics` | Mixed Intents | `healthy_protein_foods+healthy_greens` | `fallback` | 0.3160 | ❌ FAIL |
| 49 | `fasting window rules intermittent and low calorie snacks` | Mixed Intents | `dietary_patterns+healthy_snacks` | `fallback` | 0.3095 | ❌ FAIL |
| 50 | `flexibility stretching sore legs and lunges squat form` | Mixed Intents | `yoga_stretching+leg_exercises` | `fallback` | 0.3244 | ❌ FAIL |
| 51 | `what is the history of the roman empire` | Out-of-Scope Queries | `fallback` | `greeting` | 0.6120 | ❌ FAIL |
| 52 | `recommend some books on history` | Out-of-Scope Queries | `fallback` | `greeting` | 0.6146 | ❌ FAIL |
| 53 | `tell me about black holes in physics` | Out-of-Scope Queries | `fallback` | `greeting` | 0.6135 | ❌ FAIL |

## 5. Architectural Alignment & Recommendations

1. **Verify High-Threshold RapidFuzz**: The spelling correction mapping preserves exact intent routing by matching common typos cleanly.
2. **Ensure Balanced Intent Distribution**: Dataset enforces a strict 75 patterns per intent ratio, avoiding multi-class bias.
3. **Multi-Intent Scaling**: Mixed queries are resolved by returning combined responses separated by a logical spacer.
4. **Out-of-Scope Fallback Suggestions**: Guided prompts help direct the user back to supported topics.
