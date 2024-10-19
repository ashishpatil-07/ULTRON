# ULTRON - MULTIPURPOSE CHATBOT

## Table of Contents
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [Technical Details](#technical-details)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Project Directories](#project-directories)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Integration](#integrating-the-frontend-with-backend)
  - [Running the Application](#running-the-application)
- [Conclusion](#conclusion)

## Problem Statement
In today's digital world, professionals struggle with managing multiple tasks such as real-time conversation, updating social media, and extracting relevant information from websites. A solution is needed to streamline these tasks into one interface. The challenge we aim to solve is creating a CHATBOT that can efficiently perform all these tasks.

## Solution
Our solution is an AI-powered Multi-Purpose ChatBot that automates LinkedIn posting, performs web scraping for quick information access, and engages in conversational task management. The ChatBot is equipped to execute specific tasks that extend beyond general conversation.

### Features
1. **Conversational Interface:** Users can interact with the chatbot using text input.
2. **Voice Recognition:** Toggle voice recognition to input messages.
3. **Text-to-Speech:** Bot responses can be read aloud.
4. **Copy-to-Clipboard:** Users can copy bot responses.
5. **LinkedIn Posting:** Post updates on LinkedIn with images.
6. **Web Scraping:** Scrape websites for specific text.
7. **Dark Mode:** Toggle between light and dark themes.
8. **New Chat Button:** Reset the chat.

## Technical Details
- **FastAPI:** For building and managing API endpoints.
- **Python:** As the primary programming language due to its extensive libraries and ease of integration with AI models.
- **ReactJS:** For building the user interface, offering a dynamic and responsive user experience.
- **Gemini AI:** For enhancing natural language processing and user interaction.
- **HTML/CSS:** For structure and styling.
- **Fetch API:** For handling API requests.
- **Web Speech API:** For voice recognition and text-to-speech functionality.

## Setup and Installation

### Prerequisites
- Python ( Download from here: https://python.org/downloads/ )
- Google Generative AI API key ( Get your Api key from here : https://aistudio.google.com/app/apikey )
- LinkedIn API access token ( To get access token : https://towardsdatascience.com/linkedin-api-python-programmatically-publishing-d88a03f08ff1 )
- Node.js ( Get from here: https://nodejs.org/en )

### Project Directories

**PROJECT DIRECTORIES**


    multi-purpose-chatbot/
    │
    ├── BACKEND/
    │   ├── main.py
    │   ├── linkedin.py
    │   ├── web_scraper.py
    │   ├── .env
    │   ├── requirements.txt
    │   └── ...
    |
    ├── FRONTEND/
    │   ├── public/
    │   ├── src/
    │   │   ├── App.js
    │   │   ├── App.css
    │   │   ├── chatbot-logo.png
    │   │   └── ...
    │   ├── .gitignore
    │   ├── package-lock.json
    │   └── package.json
    │
    └── README.md


### Backend Setup
1. Navigate to the backend directory:
    ```bash
    cd backend
    ```

2. Create a `requirements.txt` file and add the necessary packages:
    ```text
    fastapi
    requests
    python-dotenv
    bs4
    pydantic
    uvicorn
    aiofiles
    google.generativeai
    ```

3. Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file with your API keys:
    ```text
    GEMINI_API_KEY=your_gemini_api_key_here
    LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token_here
    LINKEDIN_PROFILE_ID_URN=your_linkedin_profile_id_urn_here
    ```

5. Start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```
   The backend API will be available at `http://localhost:8000`.

### Frontend Setup
1. Open Terminal and navigate to the project folder, then create the frontend:
    ```bash
    npx create-react-app FRONTEND
    ```

2. Navigate to the frontend folder:
    ```bash
    cd FRONTEND
    ```

3. Start the frontend:
    ```bash
    npm start
    ```
   This runs the app in development mode and opens it at `http://localhost:3000`.

### Integrating the Frontend with Backend
Ensure CORS is enabled in `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
### Running the Application
 1. Make sure the backend server is running at http://127.0.0.1:8000.
 2. Start the frontend server at http://localhost:3000.
 3. Open a web browser and go to http://localhost:3000 to use the Multi-Purpose ChatBot.
   
## Conclusion
The project demonstrates a Multi-Purpose ChatBot that combines conversational AI with practical, task-oriented functionalities, showcasing a user-friendly chat interface and a flexible architecture for various use cases.

