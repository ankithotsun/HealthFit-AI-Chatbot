# CHAPTER 20: TESTING

This chapter outlines the testing strategy, test cases, and verification results for **HealthFit AI**, demonstrating the system's reliability and stability.

## 20.1 Test Plans & Strategies

The system testing strategy is divided into three tiers:
1. **Automated Unit Testing (`tests/test_nlp.py`)**:
   Runs inside `pytest` to assert that core functional code executes correctly. It covers five primary modules:
   - *Preprocessors*: Confirms punctuation removal, lowercasing, and spelling check operations.
   - *Spelling Correction*: Asserts that fuzzy matching corrects common typos (e.g. `protien`).
   - *Follow-up Intent*: Verifies intent inheritance on follow-up terms (e.g. `explain it`).
   - *Intent Aliases*: Asserts that shorthand aliases override classification.
   - *Session Memory*: Verifies profile metrics are correctly persisted and loaded.
2. **System-Level Evaluation (`tests/evaluate_model.py`)**:
   Runs unseen queries across 6 testing divisions (Clean English, Conversational, Typos, Hinglish, Mixed, Out-of-Scope) to evaluate real-world performance.
3. **Manual Verification & Boundary Testing**:
   Tests boundary inputs (e.g., negative physical values, massive inputs, and empty queries) to ensure the system handles exceptions gracefully.

## 20.2 Test Cases and Results

The table below lists the test cases executed to verify the system:

| Test ID | Test Category | Input / Action | Expected Result | Pass / Fail |
| :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Unit (Preprocessor) | `preprocess_classifier("Hello!! How's it going?")` | Output: `"hello hows it going"` (keeps stopwords). | **PASS** |
| **TC-02** | Unit (Preprocessor) | `preprocess_keywords("I am running and lifting weights")` | Output: `"run weight"` (removes stopwords, lemmatizes). | **PASS** |
| **TC-03** | Unit (Spelling) | `correct_spelling("I want protien rich diet")` | Output: `"I want protein rich diet"` (corrects spelling). | **PASS** |
| **TC-04** | Unit (Follow-up) | Msg 1: `What is my BMI?` <br> Msg 2: `explain it` | Msg 2 inherits the `bmi` intent with `confidence = 1.0`. | **PASS** |
| **TC-05** | Unit (Aliases) | Input: `fat` | Matches intent alias and returns `workout_weight_loss`. | **PASS** |
| **TC-06** | Unit (Session DB) | Msg 1: `I weigh 80 kg` <br> Msg 2: `Suggest meals` | Msg 2 uses the saved weight of `80 kg` to personalize dietary advice. | **PASS** |
| **TC-07** | Boundary | Input: empty spaces `"   "` | Handled gracefully, returning `fallback` with `0.0` confidence. | **PASS** |
| **TC-08** | Boundary | Input: `weight is -50 kg` | Negative values are rejected; prompts user to provide valid metrics. | **PASS** |
| **TC-09** | System (Out-of-Scope) | `what is the capital of france` | Overlap check returns `fallback` with `0.0` confidence. | **PASS** |
| **TC-10** | System (Emergency) | `chest pain while running` | Matches emergency disclaimer; prompts user to seek medical help immediately. | **PASS** |
| **TC-11** | Integration (UI) | Click upvote button (👍) on response | Message ID and rating (+1) are logged in the `feedback` table. | **PASS** |

### Automated Unit Test Execution Log
```bash
$ venv/bin/python -m pytest tests/test_nlp.py
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/ankit/Documents/HealthFit-AI-Chatbot
collected 5 items

tests/test_nlp.py .....                                                  [100%]

============================== 5 passed in 3.63s ===============================
```
All automated unit and system-level tests passed, demonstrating the system is highly stable and ready for deployment.
