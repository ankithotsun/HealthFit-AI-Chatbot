You are a senior software architect, full-stack developer, NLP engineer, and technical writer.

Your task is to build my final-year MCA major project from scratch and prepare the complete documentation in a university-submission format. Follow these requirements exactly.

PROJECT THEME
Create a health and fitness chatbot that answers user questions in natural language.
The chatbot must handle common queries such as:
- workout suggestions.
- diet and nutrition guidance.
- calorie estimation.
- hydration tips.
- sleep and recovery tips.
- BMI calculation.
- general fitness motivation.
- beginner exercise guidance.
- healthy eating suggestions.
- fallback answers for unknown questions.

IMPORTANT CONSTRAINTS
- Build an original project.
- Do not copy code or report text from any source.
- Keep the content plagiarism-free and written in fresh wording.
- The chatbot should provide general wellness information only.
- Add a clear disclaimer that it is not a medical diagnosis tool.
- If a user asks for emergency, severe, or diagnosis-related help, the chatbot should advise consulting a qualified doctor immediately.
- The code must be clean, commented, modular, and easy to explain in viva.
- The documentation must match a university major-project format.

RECOMMENDED TECHNOLOGY STACK
Use:
- Python 3.11+
- Flask for backend.
- HTML, CSS, Bootstrap, and JavaScript for frontend.
- SQLite for local storage.
- scikit-learn for intent classification.
- NLTK or spaCy for text preprocessing.
- JSON files for intent data and knowledge base.
- Optional: a simple rule-based layer for BMI, calorie, and hydration calculations.

PROJECT GOAL
Make a chatbot that feels practical and can answer user questions with reasonable accuracy using NLP-based intent recognition and prewritten domain responses.

FUNCTIONAL REQUIREMENTS
1. User can type a natural language health or fitness question.
2. System detects the intent.
3. System returns a relevant answer.
4. If the user asks for BMI, calculate it using height and weight.
5. If the user asks for calorie-related help, provide approximate guidance.
6. If the user asks for workout advice, suggest beginner-friendly routines.
7. If the question is unknown, show a safe fallback response.
8. Include a chat UI with a clean interface.
9. Include a conversation history display.
10. Include a reset conversation button.
11. Include a simple feedback option if possible.

NON-FUNCTIONAL REQUIREMENTS
- Fast response.
- Clear structure.
- Easy deployment on a local machine.
- Simple setup for demonstration.
- Good error handling.
- No broken links.
- No placeholder code in final deliverable.
- All files should run without missing imports or undefined variables.

PROJECT FILE STRUCTURE
Create a logical folder structure such as:
- app.py
- requirements.txt
- README.md
- /templates
- /static/css
- /static/js
- /data/intents.json
- /data/fitness_knowledge.json
- /models
- /utils
- /tests
- /docs

BUILD PROCESS
Phase 1: Planning.
- Define project title.
- Define problem statement.
- Define objectives.
- Define scope.
- Define limitations.
- Define modules.
- Define technology stack.
- Define expected output.

Phase 2: Design.
- Design the chatbot architecture.
- Design the intent flow.
- Design the database schema if needed.
- Design the UI layout.
- Design the conversation flow.
- Design fallback handling.

Phase 3: Implementation.
- First generate the full folder structure.
- Then generate the backend code.
- Then generate the NLP pipeline.
- Then generate the frontend UI.
- Then generate the data files.
- Then generate the test cases.
- Then generate the documentation files.

Phase 4: Testing.
- Add unit tests for intent detection and helper functions.
- Add test cases for BMI calculation.
- Add test cases for fallback responses.
- Verify no runtime errors.
- Verify imports.
- Verify that all pages load correctly.

Phase 5: Documentation.
Prepare original, plagiarism-free documentation with the following chapters:
1. Title Page.
2. Certificate.
3. Declaration.
4. Acknowledgement.
5. Abstract.
6. Table of Contents.
7. Introduction.
8. SDLC of the Project.
9. Design.
10. Coding & Implementation.
11. Testing.
12. Application.
13. Conclusion.
14. Bibliography in APA style.

DOCUMENTATION RULES
- Write in formal academic language.
- Keep the content original.
- Do not copy paragraphs from websites or books.
- Use clear headings and subheadings.
- Make it detailed enough for a final-year MCA submission.
- Include diagrams where useful, such as architecture, flowchart, use case, and class/module diagram.
- Include test tables with test case, expected result, and actual result.
- Include screenshots placeholders where needed.
- Include a bibliography section with legitimate references in APA style.

OUTPUT FORMAT
First, give me the project plan.
Then generate the code file by file.
Then generate the documentation chapter by chapter.
Then generate a final README with run instructions.

I want the chatbot to be easy to demo in viva, easy to explain, and stable enough to run locally without internet dependency.

Before writing code, ask me only for the project title if absolutely necessary. Otherwise, proceed with a sensible default title and continue.