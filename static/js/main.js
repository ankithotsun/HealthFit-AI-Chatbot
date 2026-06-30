/**
 * HealthFit AI Chatbot — Main Application Script
 * Vanilla JavaScript — Handles state, API calls, rendering, and DOM interactions.
 */

(function () {
    'use strict';

    // =====================================================================
    // State Management
    // =====================================================================
    const state = {
        currentSessionId: null,
        sessionsList: [], // Array of objects: { id, title, timestamp }
        isAwaitingResponse: false
    };

    // API Route Base URLs
    const API = {
        chat: '/api/chat',
        history: '/api/history',
        feedback: '/api/feedback'
    };

    // =====================================================================
    // DOM Elements Cache
    // =====================================================================
    const el = {
        chatMessages: document.getElementById('chat-messages'),
        chatForm: document.getElementById('chat-form'),
        chatInput: document.getElementById('chat-input'),
        btnSend: document.getElementById('btn-send'),
        btnSendText: document.getElementById('btn-send-text'),
        btnSendSpinner: document.getElementById('btn-send-spinner'),
        charCounter: document.getElementById('char-counter'),
        typingIndicator: document.getElementById('typing-indicator'),
        sessionBadge: document.getElementById('session-badge'),
        historyList: document.getElementById('history-list'),
        historyEmptyState: document.getElementById('history-empty-state'),
        btnNewChat: document.getElementById('btn-new-chat'),
        btnClearChat: document.getElementById('btn-clear-chat'),
        suggestedQuestions: document.getElementById('suggested-questions'),
        
        // Sidebar controls (responsive)
        btnSidebarToggle: document.getElementById('btn-sidebar-toggle'),
        btnSidebarClose: document.getElementById('btn-sidebar-close'),
        chatSidebar: document.getElementById('chat-sidebar'),
        
        // Toast notifications
        toastContainer: document.getElementById('toast-container'),
        errorToast: document.getElementById('error-toast'),
        toastMessage: document.getElementById('toast-message')
    };

    // Bootstrap toast instance
    let bootstrapToast = null;

    // =====================================================================
    // Initialization & Event Binding
    // =====================================================================
    document.addEventListener('DOMContentLoaded', () => {
        // Init Bootstrap Toast
        if (el.errorToast) {
            bootstrapToast = new bootstrap.Toast(el.errorToast);
        }

        initSession();
        bindEvents();
        loadActiveChatHistory();
        renderSessionsSidebar();
    });

    // =====================================================================
    // Event Listeners
    // =====================================================================
    function bindEvents() {
        // Chat Form Submission
        el.chatForm.addEventListener('submit', handleFormSubmit);

        // Input keyup for Character Counter
        el.chatInput.addEventListener('input', updateCharCounter);

        // Suggested questions chips
        el.suggestedQuestions.addEventListener('click', handleSuggestedClick);

        // New Chat action
        el.btnNewChat.addEventListener('click', handleNewChat);

        // Clear Chat History action
        el.btnClearChat.addEventListener('click', handleClearChat);

        // Responsive Sidebar Toggle
        el.btnSidebarToggle.addEventListener('click', () => {
            el.chatSidebar.classList.add('open');
        });

        el.btnSidebarClose.addEventListener('click', () => {
            el.chatSidebar.classList.remove('open');
        });

        // Close sidebar if user clicks outside of it on mobile
        document.addEventListener('click', (event) => {
            const isClickInsideSidebar = el.chatSidebar.contains(event.target);
            const isClickToggle = el.btnSidebarToggle.contains(event.target);
            if (!isClickInsideSidebar && !isClickToggle && el.chatSidebar.classList.contains('open')) {
                el.chatSidebar.classList.remove('open');
            }
        });
    }

    // =====================================================================
    // Session Operations
    // =====================================================================
    
    /**
     * Initializes or recovers the active session ID.
     */
    function initSession() {
        // Try to read active session from LocalStorage
        let activeSession = localStorage.getItem('healthfit_active_session');
        
        // Read the history sessions list
        let savedSessions = localStorage.getItem('healthfit_sessions_list');
        if (savedSessions) {
            try {
                state.sessionsList = JSON.parse(savedSessions);
            } catch (e) {
                state.sessionsList = [];
            }
        }

        if (!activeSession) {
            // Generate a fresh session ID on first load
            activeSession = generateSessionId();
            localStorage.setItem('healthfit_active_session', activeSession);
            
            // Add to session list tracking
            addSessionToList(activeSession, "New Conversation");
        }

        state.currentSessionId = activeSession;
        updateSessionBadge();
    }

    /**
     * Generates a random session ID based on timestamp and randomness.
     */
    function generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substring(2, 9);
    }

    /**
     * Updates the UI badge displaying the session ID.
     */
    function updateSessionBadge() {
        if (el.sessionBadge) {
            const shortId = state.currentSessionId.replace('session_', '').substring(0, 10);
            el.sessionBadge.textContent = `ID: ${shortId}...`;
            el.sessionBadge.title = `Full Session ID: ${state.currentSessionId}`;
        }
    }

    /**
     * Adds a session to our tracking list in localStorage.
     */
    function addSessionToList(sessionId, title) {
        // Guard check for duplicates
        if (state.sessionsList.some(s => s.id === sessionId)) return;

        const newSession = {
            id: sessionId,
            title: title || "New Conversation",
            timestamp: new Date().toISOString()
        };

        state.sessionsList.unshift(newSession); // Add to beginning of history
        saveSessionsToLocalStorage();
    }

    function saveSessionsToLocalStorage() {
        localStorage.setItem('healthfit_sessions_list', JSON.stringify(state.sessionsList));
    }

    /**
     * Re-renders the sidebar session history panel.
     */
    function renderSessionsSidebar() {
        // Clear except empty state
        const items = el.historyList.querySelectorAll('.history-item');
        items.forEach(item => item.remove());

        if (state.sessionsList.length === 0) {
            el.historyEmptyState.classList.remove('d-none');
            return;
        }

        el.historyEmptyState.classList.add('d-none');

        state.sessionsList.forEach(session => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = `list-group-item list-group-item-action history-item ${session.id === state.currentSessionId ? 'active' : ''}`;
            btn.dataset.id = session.id;
            
            // Format time
            const date = new Date(session.timestamp);
            const timeStr = date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) + ' ' + 
                            date.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', hour12: true });

            btn.innerHTML = `
                <i class="bi bi-chat-left-text-fill"></i>
                <div class="flex-grow-1 text-truncate text-start">
                    <div class="fw-medium text-truncate fs-7">${session.title}</div>
                    <small class="text-muted font-monospace fs-8 d-block mt-0.5">${timeStr}</small>
                </div>
            `;

            // Click sidebar session item to switch conversations
            btn.addEventListener('click', () => switchSession(session.id));
            el.historyList.appendChild(btn);
        });
    }

    /**
     * Switches the active session to the selected session ID.
     */
    function switchSession(sessionId) {
        if (state.isAwaitingResponse) return; // Prevent switching while request is in flight
        if (state.currentSessionId === sessionId) return;

        state.currentSessionId = sessionId;
        localStorage.setItem('healthfit_active_session', sessionId);
        
        updateSessionBadge();
        renderSessionsSidebar();
        loadActiveChatHistory();
        
        // Close sidebar on mobile after clicking
        el.chatSidebar.classList.remove('open');
    }

    // =====================================================================
    // UI Event Handlers
    // =====================================================================

    /**
     * Starts a completely clean chat session.
     */
    function handleNewChat() {
        if (state.isAwaitingResponse) return;

        // Generate and set new session ID
        const newSessionId = generateSessionId();
        state.currentSessionId = newSessionId;
        localStorage.setItem('healthfit_active_session', newSessionId);

        // Add to tracking list
        addSessionToList(newSessionId, "New Conversation");

        updateSessionBadge();
        renderSessionsSidebar();
        
        // Reset Chat UI
        clearChatUI();
        showWelcomeCard();
        el.chatInput.value = '';
        updateCharCounter();
        
        el.chatSidebar.classList.remove('open');
    }

    /**
     * Clears all messages from the screen.
     */
    function clearChatUI() {
        // Keep only welcome card and typing indicator
        const messages = el.chatMessages.querySelectorAll('.msg-row, .welcome-card');
        messages.forEach(m => m.remove());
    }

    function showWelcomeCard() {
        // If welcome card doesn't exist on page, we can recreate it or show/hide
        // Simply reload page content or append welcome template
        const welcomeHtml = `
            <div class="welcome-card card border-0 shadow-sm mx-auto my-4 text-center max-w-600">
                <div class="card-body p-4 p-md-5">
                    <div class="welcome-icon bg-success-subtle text-success rounded-circle d-flex align-items-center justify-content-center mx-auto mb-3">
                        <i class="bi bi-activity fs-2"></i>
                    </div>
                    <h2 class="card-title fw-bold text-dark fs-4 mb-2">Welcome to HealthFit AI!</h2>
                    <p class="card-text text-secondary mb-4">
                        I am your personal NLP-based wellness and fitness assistant. Ask me questions about workout routines, nutritional plans, calorie counts, hydration, or calculate your BMI!
                    </p>
                    <hr class="my-4 text-muted">
                    <h3 class="fs-6 fw-semibold text-dark text-start mb-3">Suggested Topics:</h3>
                    <div class="d-flex flex-wrap gap-2 justify-content-start" id="suggested-questions-dynamic">
                        <button type="button" class="btn btn-sm btn-outline-success suggested-pill" data-question="Calculate my BMI">
                            <i class="bi bi-calculator me-1"></i> Calculate my BMI
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-success suggested-pill" data-question="What is a good beginner workout?">
                            <i class="bi bi-lightning-charge me-1"></i> Beginner Workouts
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-success suggested-pill" data-question="Suggest a healthy protein-rich dinner">
                            <i class="bi bi-egg-fried me-1"></i> Healthy Dinner Plan
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-success suggested-pill" data-question="How much water should I drink daily?">
                            <i class="bi bi-droplet me-1"></i> Hydration Advice
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-success suggested-pill" data-question="How can I manage stress and sleep better?">
                            <i class="bi bi-moon-stars me-1"></i> Stress & Sleep
                        </button>
                    </div>
                </div>
            </div>
        `;
        el.chatMessages.innerHTML = welcomeHtml;
        
        // Re-bind suggested pills
        const dynPills = document.getElementById('suggested-questions-dynamic');
        if (dynPills) {
            dynPills.addEventListener('click', handleSuggestedClick);
        }
    }

    /**
     * Triggers DELETE /api/history to clear database records for the session.
     */
    async function handleClearChat() {
        if (state.isAwaitingResponse) return;

        const confirmClear = confirm("Are you sure you want to delete all chat history and feedback logs for this session? This action cannot be undone.");
        if (!confirmClear) return;

        try {
            const response = await fetch(API.history, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: state.currentSessionId })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || "Failed to clear history on backend.");
            }

            // Remove this session from our local storage lists
            state.sessionsList = state.sessionsList.filter(s => s.id !== state.currentSessionId);
            saveSessionsToLocalStorage();

            // Clear UI, switch to a fresh conversation
            clearChatUI();
            
            // Generate a fresh session ID instead of staying on the deleted one
            const newSessionId = generateSessionId();
            state.currentSessionId = newSessionId;
            localStorage.setItem('healthfit_active_session', newSessionId);
            addSessionToList(newSessionId, "New Conversation");

            updateSessionBadge();
            renderSessionsSidebar();
            showWelcomeCard();
            
        } catch (err) {
            showErrorToast(err.message || "Failed to delete chat history.");
        }
    }

    /**
     * Handles clicks on starter questions.
     */
    function handleSuggestedClick(e) {
        const btn = e.target.closest('.suggested-pill');
        if (!btn) return;

        const question = btn.dataset.question;
        if (question) {
            el.chatInput.value = question;
            updateCharCounter();
            el.chatForm.dispatchEvent(new Event('submit'));
        }
    }

    /**
     * Updates character counter display.
     */
    function updateCharCounter() {
        const count = el.chatInput.value.length;
        el.charCounter.textContent = `${count} / 250 characters`;
        if (count >= 240) {
            el.charCounter.classList.add('text-danger');
            el.charCounter.classList.remove('text-muted');
        } else {
            el.charCounter.classList.remove('text-danger');
            el.charCounter.classList.add('text-muted');
        }
    }

    // =====================================================================
    // API Communication & Message Processing
    // =====================================================================

    /**
     * Handles user message submission.
     */
    async function handleFormSubmit(e) {
        e.preventDefault();

        const message = el.chatInput.value.trim();
        if (!message || state.isAwaitingResponse) return;

        // 1. Update Title in history if it's the first message
        const currentSession = state.sessionsList.find(s => s.id === state.currentSessionId);
        if (currentSession && currentSession.title === "New Conversation") {
            currentSession.title = message.substring(0, 30) + (message.length > 30 ? '...' : '');
            saveSessionsToLocalStorage();
            renderSessionsSidebar();
        }

        // 2. Clear welcome card on first user message
        const welcome = el.chatMessages.querySelector('.welcome-card');
        if (welcome) welcome.remove();

        // 3. Append User bubble
        appendMessageBubble('user', message, new Date().toISOString());
        
        // Reset input immediately
        el.chatInput.value = '';
        updateCharCounter();
        scrollToBottom();

        // 4. Trigger Bot Request pipeline
        await sendChatRequest(message);
    }

    /**
     * Submits a message to POST /api/chat.
     */
    async function sendChatRequest(message) {
        setLoadingState(true);

        try {
            const response = await fetch(API.chat, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    session_id: state.currentSessionId
                })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || "An API server error occurred.");
            }

            const data = await response.json(); // { response, intent, confidence, chat_id, entities }
            
            // Append bot bubble with returned data
            appendMessageBubble('bot', data.response, new Date().toISOString(), {
                chatId: data.chat_id,
                intent: data.intent,
                confidence: data.confidence,
                entities: data.entities
            });

            // Update user message's entity badges (if entities were extracted)
            // We append entity tags to the LAST user bubble to show what was parsed
            if (data.entities) {
                const userMessages = el.chatMessages.querySelectorAll('.msg-row.user-msg');
                if (userMessages.length > 0) {
                    const lastUserMsgRow = userMessages[userMessages.length - 1];
                    const bubble = lastUserMsgRow.querySelector('.bubble');
                    
                    // Render entity badges inside the user bubble container
                    const entitiesHtml = renderEntityBadges(data.entities);
                    if (entitiesHtml) {
                        bubble.insertAdjacentHTML('beforeend', entitiesHtml);
                    }
                }
            }

            scrollToBottom();

        } catch (err) {
            showErrorToast(err.message || "Failed to receive message from server.");
            // Append error bubble
            appendMessageBubble('bot', "I'm having trouble communicating with my analytical services. Please check if the Flask server is running.", new Date().toISOString(), { error: true });
            scrollToBottom();
        } finally {
            setLoadingState(false);
        }
    }

    /**
     * Retrieves chat logs from GET /api/history.
     */
    async function loadActiveChatHistory() {
        // Reset screen state
        clearChatUI();
        
        setLoadingState(true);

        try {
            const response = await fetch(`${API.history}?session_id=${state.currentSessionId}`);
            if (!response.ok) {
                throw new Error("Unable to retrieve session history.");
            }

            const data = await response.json(); // { history: [...] }
            
            if (data.history && data.history.length > 0) {
                data.history.forEach(item => {
                    // 1. Append User bubble
                    appendMessageBubble('user', item.user_message, item.timestamp);
                    // 2. Append Bot bubble
                    appendMessageBubble('bot', item.bot_response, item.timestamp, {
                        chatId: item.id,
                        intent: item.detected_intent,
                        confidence: item.confidence_score,
                        historical: true // Don't trigger feedback highlights if they were already rated
                    });
                });
                scrollToBottom();
            } else {
                showWelcomeCard();
            }

        } catch (err) {
            showErrorToast(err.message || "Could not retrieve chat history from server.");
            showWelcomeCard();
        } finally {
            setLoadingState(false);
        }
    }

    /**
     * Submits thumbs rating to POST /api/feedback.
     */
    async function submitFeedback(chatId, rating, clickedBtn) {
        try {
            const response = await fetch(API.feedback, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    chat_id: chatId,
                    rating: rating // 1 = thumbs up, 0 = thumbs down
                })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || "Failed to log feedback.");
            }

            // Visual feedback toggle
            const parent = clickedBtn.closest('.feedback-actions');
            const likeBtn = parent.querySelector('.btn-like');
            const dislikeBtn = parent.querySelector('.btn-dislike');

            if (rating === 1) {
                likeBtn.classList.add('active-like');
                dislikeBtn.classList.remove('active-dislike');
            } else {
                dislikeBtn.classList.add('active-dislike');
                likeBtn.classList.remove('active-like');
            }

        } catch (err) {
            showErrorToast(err.message || "Feedback submittal failed.");
        }
    }

    // =====================================================================
    // Loading, Toasts, Scrolling & Utilities
    // =====================================================================

    function setLoadingState(isLoading) {
        state.isAwaitingResponse = isLoading;
        if (isLoading) {
            el.btnSend.setAttribute('disabled', 'true');
            el.chatInput.setAttribute('readonly', 'true');
            el.btnSendText.classList.add('d-none');
            el.btnSendSpinner.classList.remove('d-none');
            el.typingIndicator.classList.remove('d-none');
        } else {
            el.btnSend.removeAttribute('disabled');
            el.chatInput.removeAttribute('readonly');
            el.btnSendSpinner.classList.add('d-none');
            el.btnSendText.classList.remove('d-none');
            el.typingIndicator.classList.add('d-none');
        }
    }

    function scrollToBottom() {
        el.chatMessages.scrollTop = el.chatMessages.scrollHeight;
    }

    function showErrorToast(message) {
        if (el.toastMessage && bootstrapToast) {
            el.toastMessage.textContent = message;
            bootstrapToast.show();
        }
    }

    // =====================================================================
    // Bubble Rendering & Formatting Helpers
    // =====================================================================

    /**
     * Appends a message bubble inside the messages container.
     */
    function appendMessageBubble(sender, text, timestamp, meta = {}) {
        const row = document.createElement('div');
        row.className = `msg-row ${sender}-msg`;

        const time = new Date(timestamp);
        const displayTime = time.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', hour12: true });

        let contentHtml = formatResponseText(text);

        if (sender === 'user') {
            row.innerHTML = `
                <div class="bubble-wrapper">
                    <div class="bubble">${contentHtml}</div>
                    <div class="msg-meta">
                        <span>${displayTime}</span>
                    </div>
                </div>
            `;
        } else {
            // Check if error bubble or regular bot bubble
            let feedbackHtml = '';
            let metadataHtml = '';
            
            if (!meta.error && meta.chatId) {
                // Regular bot bubble has 👍 / 👎 buttons
                feedbackHtml = `
                    <div class="feedback-actions">
                        <button type="button" class="btn-feedback btn-like" title="This was helpful" data-chat-id="${meta.chatId}">
                            <i class="bi bi-hand-thumbs-up-fill"></i>
                        </button>
                        <button type="button" class="btn-feedback btn-dislike" title="This was not helpful" data-chat-id="${meta.chatId}">
                            <i class="bi bi-hand-thumbs-down-fill"></i>
                        </button>
                    </div>
                `;

                if (meta.intent) {
                    const intents = meta.intent.split('+');
                    const primary = intents[0];
                    metadataHtml += `<span class="badge bg-light text-secondary border fs-8 font-monospace ms-2" title="Primary Intent">Primary: ${primary}</span>`;
                    if (intents.length > 1) {
                        const secondary = intents[1];
                        metadataHtml += `<span class="badge bg-light text-secondary border fs-8 font-monospace ms-2" title="Secondary Intent">Secondary: ${secondary}</span>`;
                    }
                }
                if (meta.entities) {
                    const entitiesList = [];
                    if (meta.entities.age) entitiesList.push(`Age: ${meta.entities.age}`);
                    if (meta.entities.gender) entitiesList.push(`Gender: ${meta.entities.gender}`);
                    if (meta.entities.height) entitiesList.push(`Height: ${meta.entities.height}`);
                    if (meta.entities.weight) entitiesList.push(`Weight: ${meta.entities.weight}`);
                    if (meta.entities.food_names && meta.entities.food_names.length > 0) {
                        entitiesList.push(`Food: ${meta.entities.food_names.join(', ')}`);
                    }
                    if (meta.entities.exercise_names && meta.entities.exercise_names.length > 0) {
                        entitiesList.push(`Activity: ${meta.entities.exercise_names.join(', ')}`);
                    }
                    if (meta.entities.fitness_goals && meta.entities.fitness_goals.length > 0) {
                        entitiesList.push(`Goal: ${meta.entities.fitness_goals.join(', ').replace(/_/g, ' ')}`);
                    }
                    if (entitiesList.length > 0) {
                        metadataHtml += `<span class="badge bg-light text-secondary border fs-8 font-monospace ms-2" title="Extracted Entities">Entities: ${entitiesList.join(' | ')}</span>`;
                    }
                }
            }

            row.innerHTML = `
                <div class="bubble-wrapper">
                    <div class="bubble">${contentHtml}</div>
                    <div class="msg-meta">
                        <span>${displayTime}</span>
                        ${metadataHtml}
                        ${feedbackHtml}
                    </div>
                </div>
            `;

            // Bind feedback button event listeners for active interaction
            if (!meta.error && meta.chatId) {
                const likeBtn = row.querySelector('.btn-like');
                const dislikeBtn = row.querySelector('.btn-dislike');
                
                likeBtn.addEventListener('click', () => submitFeedback(meta.chatId, 1, likeBtn));
                dislikeBtn.addEventListener('click', () => submitFeedback(meta.chatId, 0, dislikeBtn));
            }
        }

        el.chatMessages.appendChild(row);
    }

    /**
     * Escapes XML/HTML text and formats simple markdown-style lists or paras into HTML.
     */
    function formatResponseText(text) {
        if (!text) return '';

        // Escape HTML to prevent XSS injection
        let escaped = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

        // Parse lists and paragraphs line by line
        let lines = escaped.split('\n');
        let inList = false;
        let inNumList = false;
        let htmlResult = [];

        for (let line of lines) {
            const trimmedLine = line.trim();

            if (!trimmedLine) {
                if (inList) { htmlResult.push('</ul>'); inList = false; }
                if (inNumList) { htmlResult.push('</ol>'); inNumList = false; }
                htmlResult.push('<br>');
                continue;
            }

            // Matches bullet lists: starts with '- ' or '* '
            if (trimmedLine.startsWith('- ') || trimmedLine.startsWith('* ')) {
                if (inNumList) { htmlResult.push('</ol>'); inNumList = false; }
                if (!inList) { htmlResult.push('<ul class="mb-2">'); inList = true; }
                htmlResult.push(`<li>${trimmedLine.substring(2)}</li>`);
            } 
            // Matches numbered lists: starts with "1. " or "2. " etc.
            else if (/^\d+\.\s/.test(trimmedLine)) {
                if (inList) { htmlResult.push('</ul>'); inList = false; }
                if (!inNumList) { htmlResult.push('<ol class="mb-2">'); inNumList = true; }
                const itemContent = trimmedLine.replace(/^\d+\.\s/, '');
                htmlResult.push(`<li>${itemContent}</li>`);
            } 
            // Regular text block
            else {
                if (inList) { htmlResult.push('</ul>'); inList = false; }
                if (inNumList) { htmlResult.push('</ol>'); inNumList = false; }
                htmlResult.push(`<p class="mb-2">${trimmedLine}</p>`);
            }
        }

        // Close any dangling lists
        if (inList) htmlResult.push('</ul>');
        if (inNumList) htmlResult.push('</ol>');

        // Clean redundant break tags and return
        return htmlResult.join('').replace(/(<br>){2,}/g, '<br>');
    }

    /**
     * Renders small metadata badges for extracted entities.
     */
    function renderEntityBadges(entities) {
        if (!entities) return '';
        let badgesHtml = [];

        if (entities.age) {
            badgesHtml.push(`<span class="badge bg-primary entity-badge" title="Age extracted from query"><i class="bi bi-calendar"></i> Age: ${entities.age}</span>`);
        }
        if (entities.gender) {
            badgesHtml.push(`<span class="badge bg-info text-dark entity-badge" title="Gender extracted from query"><i class="bi bi-person"></i> Gender: ${entities.gender}</span>`);
        }
        if (entities.height) {
            badgesHtml.push(`<span class="badge bg-secondary entity-badge" title="Height extracted from query"><i class="bi bi-rulers"></i> Height: ${entities.height}</span>`);
        }
        if (entities.weight) {
            badgesHtml.push(`<span class="badge bg-dark entity-badge" title="Weight extracted from query"><i class="bi bi-speedometer2"></i> Weight: ${entities.weight}</span>`);
        }
        
        if (entities.food_names && entities.food_names.length > 0) {
            entities.food_names.forEach(food => {
                badgesHtml.push(`<span class="badge bg-success entity-badge" title="Food item extracted"><i class="bi bi-egg-fried"></i> Food: ${food}</span>`);
            });
        }
        
        if (entities.exercise_names && entities.exercise_names.length > 0) {
            entities.exercise_names.forEach(ex => {
                badgesHtml.push(`<span class="badge bg-warning text-dark entity-badge" title="Exercise tag extracted"><i class="bi bi-bicycle"></i> Activity: ${ex}</span>`);
            });
        }
        
        if (entities.quantities && entities.quantities.length > 0) {
            entities.quantities.forEach(q => {
                badgesHtml.push(`<span class="badge bg-light text-dark border entity-badge" title="Quantity extracted"><i class="bi bi-hash"></i> Qty: ${q}</span>`);
            });
        }
        
        if (entities.fitness_goals && entities.fitness_goals.length > 0) {
            entities.fitness_goals.forEach(goal => {
                const readableGoal = goal.replace('_', ' ');
                badgesHtml.push(`<span class="badge bg-danger entity-badge" title="Fitness Goal extracted"><i class="bi bi-trophy"></i> Goal: ${readableGoal}</span>`);
            });
        }

        if (badgesHtml.length === 0) return '';
        return `<div class="entity-badges mt-2">${badgesHtml.join('')}</div>`;
    }

})();
