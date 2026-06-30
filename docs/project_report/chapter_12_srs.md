# CHAPTER 12: SOFTWARE REQUIREMENT SPECIFICATION (SRS)

This Software Requirement Specification (SRS) details the hardware, software, functional, and non-functional requirements necessary to develop, deploy, and execute **HealthFit AI**.

## 12.1 Hardware Requirements

### 1. Development Environment (Client & Host Machine)
* **Processor**: Intel Core i5 / AMD Ryzen 5 or higher (multicore processor).
* **RAM**: 8 GB minimum (16 GB recommended for running concurrent test suites and IDEs).
* **Storage**: 10 GB of available solid-state drive (SSD) space.
* **Network**: Active internet connection for library downloads (NLTK corpora, pip packages).

### 2. Production Deployment Environment (Hosting Server)
* **Processor**: Single-core virtual CPU (vCPU) or higher.
* **RAM**: 1 GB minimum (standard cloud VM instances like AWS EC2 t3.micro or equivalent).
* **Storage**: 2 GB of SSD space.

## 12.2 Software Requirements

### 1. Operating System
* Windows 10/11, macOS (10.15 Catalina or newer), or Linux (Ubuntu 20.04 LTS or newer).

### 2. Backend Environment & Programming Language
* **Python Runtime**: Python 3.9 or higher.
* **Web Framework**: Flask 3.0.x (lightweight WSGI web application framework).
* **Database Engine**: SQLite 3 (serverless, file-backed relational database).

### 3. Key Library Dependencies (Python packages)
* **scikit-learn**: For TF-IDF Vectorizer and Logistic Regression training.
* **nltk**: Natural Language Toolkit for tokenization, stopword filtering, lemmatization, and WordNet.
* **rapidfuzz**: For spelling correction and string distance evaluations.
* **pytest**: For automated test runner framework.
* **joblib**: For serialization and deserialization of machine learning models.

### 4. Frontend Technologies
* **Structure & Markup**: HTML5 (semantic layout).
* **Styling & Presentation**: CSS3 & Bootstrap 5 (responsive utility-first layout).
* **Logic & Interactivity**: Vanilla Javascript (ES6+, asynchronous Fetch API, DOM manipulation).

## 12.3 Functional and Non-Functional Requirements

### 1. Functional Requirements
* **FR-1: User Message Processing**: The system must accept natural language text input from the user through the chat interface.
* **FR-2: Intent Classification**: The NLP engine must classify incoming queries into one of the 34 predefined intents with confidence scores.
* **FR-3: Dynamic Calculations**: The system must calculate BMI, BMR, and water requirements dynamically when the required physical metrics are supplied.
* **FR-4: State Persistence**: The backend must save and load height, weight, age, gender, and fitness goal variables in a persistent session profile database.
* **FR-5: Contextual Recovery**: If a user submits a vague query (e.g., *"tell me more"*), the system must query chat history and inherit the previous intent.
* **FR-6: Feedback Loop**: Users must be able to upvote (👍) or downvote (👎) bot responses, storing the results in the database for auditing.
* **FR-7: Session Panel**: The UI must display a sidebar listing all active chat sessions, allowing users to start new sessions or clear current history.

### 2. Non-Functional Requirements
* **NFR-1: Performance (Latency)**: The system must process queries and return response messages in less than 200 milliseconds (under local testing, actual average is <100ms).
* **NFR-2: Responsiveness (UI)**: The front-end interface must scale gracefully across mobile screens, tablets, and desktop devices using Bootstrap grid breakpoints.
* **NFR-3: Reliability**: The chatbot must handle invalid parameters (e.g., negative height or text in numeric fields) without throwing uncaught server errors (500), returning polite error tips instead.
* **NFR-4: Maintainability**: The code must adhere to clean-code standards, separating database logic (`db_manager.py`), classifier execution (`classifier.py`), and routes (`app.py`).
* **NFR-5: Plagiarism & Originality**: The documentation and source code must adhere to academic integrity, passing standard plagiarism checking utilities.
