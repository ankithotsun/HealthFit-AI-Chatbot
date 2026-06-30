# USER MANUAL: HEALTHFIT AI CHATBOT

This user manual guides you through using the **HealthFit AI** conversational chatbot.

## 1. Getting Started
1. Open your web browser and navigate to the application URL (typically `http://127.0.5.1:5000` when running locally).
2. The browser will render the emerald-themed chatbot dashboard. A greeting message from **HealthFit AI** will appear in the main chat panel.

## 2. Conversing with the Chatbot
1. Locate the text input bar at the bottom of the interface.
2. Type your query in natural language. For example:
   - *"How to lose weight?"*
   - *"What should I eat for a healthy breakfast?"*
   - *"Can you give me a beginner gym routine?"*
3. Press **Enter** on your keyboard or click the **Send** button.
4. While the bot processes your message, a three-dot typing indicator animation will appear. The response will be delivered in under 100ms.

## 3. Entering and Tracking Physical Metrics
HealthFit AI personalizes its advice if you supply your physical stats.
1. Type a message containing your metrics, such as:
   - *"I weigh 80 kg and my height is 180 cm. What is my BMI?"*
2. The chatbot will calculate your BMI (`24.69`, Normal Weight) and display it.
3. Observe the top of the interface: small green badges indicating **Weight: 80 kg** and **Height: 180 cm** will automatically update.
4. Future advice (e.g. daily water requirements or calories) will automatically refer to these stored parameters.

## 4. Submitting Response Feedback
To help improve the chatbot's accuracy:
1. Hover over or tap any response bubble sent by the chatbot.
2. Two feedback icons—Thumbs Up (👍) and Thumbs Down (👎)—will appear.
3. Click **👍** if the advice was helpful, or **👎** if it was incorrect or irrelevant.
4. Your feedback will be recorded silently in the database.

## 5. Managing Chat Sessions
* **New Chat**: Click the **"+ New Chat"** button in the sidebar to open a clean chat canvas.
* **Clear Chat**: Click **"Clear History"** to delete all saved transcripts from your current session.
* **Session History**: Use the sidebar panel to click and switch between older chat conversations.
* **Metric Overrides**: If you want to update your height or weight, simply type a new message containing the metrics (e.g., *"my weight changed to 75 kg"*), and the badges will update instantly.
