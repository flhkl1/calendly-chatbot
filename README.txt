
Calendly Chatbot

This Calendly Chatbot offers a dynamic interface for users to manage their Calendly events through text commands. It leverages OpenAI's GPT-3.5 to interpret and respond to user inputs, facilitating actions like listing and canceling scheduled events.

Features
1. Real-time Interaction: Engages users via WebSocket for immediate communication.
2. Event Management: Allows users to view and cancel their Calendly events.
3. Secure Session Management: Maintains sessions with unique IDs and uses HTTP-only cookies for enhanced security.

Setup
Launch the server:
1. uvicorn main:app --reload

Usage
1. Start a Session: Initialize through /start to get a session ID.
2. WebSocket Communication: Connect via /ws using the session cookie.
3. HTTP Interaction: Send commands through /chat for managing events.

API Endpoints
1. POST /start: Initializes a user session.
2. WebSocket /ws: Manages real-time chat interactions.
3. GET /chat: Handles event management commands based on session cookies.

Use simple commands like "Show me the scheduled events" and "Cancel my event at 3pm" to interact with the chatbot. This setup ensures a user-friendly approach to managing Calendly events efficiently.