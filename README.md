# ULTRON - MULTIPURPOSE CHATBOT

**Problem Statement:**
In today's digital world, professionals often struggle with managing multiple task such as real-time conversation, updating social media also extracting relevant information from websites.  A solution is needed to streamline these tasks into one interface.
"The challenge we aim to solve is creating a CHATBOT which can do all this tasks efficiently".

**Solution:**
"Our solution is an AI-powered Multi-Purpose ChatBot that automates LinkedIn posting, performs web scraping for quick information access, and engages in conversational task management."
 The ChatBot is equipped to execute specific tasks that extend beyond general conversation:
   1.  Update a Post on LinkedIn: The ChatBot should be capable of interfacing with LinkedIn to post updates or articles about specified topics, using provided API        access.
   2.  Web Scrape a Website and Search for Occurrences of a Text: The bot should perform web scraping activities to search websites for specific text or patterns,         providing the results back to the user in a concise format.

**Features :**
  1. Conversational Interface: Users can interact with the chatbot using text input.
  2. Voice Recognition: Users can toggle voice recognition to input messages.
  3. Text-to-Speech: Bot responses can be read aloud.
  4. Copy-to-Clipboard: Users can copy bot responses.
  5. LinkedIn Posting: Users can post updates on LinkedIn with one or more images.
  6. Web Scraping: Users can scrape websites for specific text.
  7. Dark Mode: Users can toggle between light and dark themes.
  8. New Chat Button: Users can reset the chat.

**Technical Details :**
  1. FastAPI for building and managing API endpoints.
  2. Python as the primary programming language due to its extensive libraries and ease of integration with AI models.
  3. ReactJS for building the user interface, offering a dynamic and responsive user experience.
  4. Gemini AI will enable natural language processing, enhancing user interaction and making the chatbot capable of responding to user queries effectively.
  5. HTML/CSS: Structure and styling.
  6. Fetch API: Handles API requests.
  7. Web Speech API: Enables voice recognition and text-to-speech.

**Key Achievements :**
  1. The ChatBot successfully combined general conversational AI with task-specific functions, demonstrating its versatility.
  2. The integration of FastAPI and ReactJS enabled smooth communication between the frontend and backend, providing a user-friendly interface.

**Conclusion :**
The project demonstrated the Multi-Purpose ChatBot that combines conversational AI with practical, task-oriented functionalities. It showcased a user-friendly chat interface and a flexible architecture that can be expanded to accommodate various use cases in both professional and personal contexts.

## Setup and Installation

### Prerequisites
- Python 3.7+ (for FastAPI backend)
- Google Generative AI API key
- LinkedIn API access token

### Backend Setup

1. Navigate to the backend directory:
     cd backend
   
2. Create a virtual environment and activate it:
     python -m venv venv
     source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install required Python packages:
     pip install fastapi uvicorn python-dotenv google-generativeai

5. Create a `.env` file in the backend directory with your API keys:
   
   
6. Start the FastAPI server:
     uvicorn main:app --reload

The backend API will be available at `http://localhost:8000`.
