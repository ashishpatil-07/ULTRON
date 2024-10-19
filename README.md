# ULTRON - MULTIPURPOSE CHATBOT

## Table of Contents
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [Technical Details](#technical-details)
- [Key Achievements](#key-achievements)
- [Conclusion](#conclusion)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Project Directories](#project-directories)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Integration](#integrating-the-frontend-with-backend)
  - [Running the Application](#running-the-application)
- [Usage](#usage)

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

## Key Achievements
1. Successfully combined general conversational AI with task-specific functions, demonstrating versatility.
2. Integration of FastAPI and ReactJS enabled smooth communication between the frontend and backend, providing a user-friendly interface.

## Conclusion
The project demonstrates a Multi-Purpose ChatBot that combines conversational AI with practical, task-oriented functionalities, showcasing a user-friendly chat interface and a flexible architecture for various use cases.

## Setup and Installation

### Prerequisites
- Python 3.7+
- Google Generative AI API key
- LinkedIn API access token
- Node.js

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

**Backend Setup**

1. Navigate to the backend directory:
   
       cd backend
   
3. Create a file as requirements.txt and add the following things:
   
       fastapi
       requests
       python-dotenv
       bs4
       pydantic
       uvicorn
       aiofiles
       google.generativeai

4. Install required Python packages:
   
       pip install -r requirements.txt  

5. Create a `.env` file in the backend directory with your API keys:

   
       GEMINI_API_KEY=your_gemini_api_key_here  # Gemini API key
       LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token_here # LinkedIn API access token
       LINKEDIN_PROFILE_ID_URN=your_linkedin_profile_id_urn_here  # LinkedIn Profile ID URN
   
6. Start the FastAPI server:
   
        uvicorn main:app --reload

The backend API will be available at `http://localhost:8000`.

**Frontend Setup**
1. Open Terminal and navigate to multipurpose chatbot folder and write this:
   
        npx create-react-app FRONTEND
   
   => this will create the frontend folder in the Chatbot folder and install necessary libraries
2. Navigate to the frontend folder:
   
         cd ../FRONTEND
3.  Execute this command :
   
         npm start
    
   this runs the app in the development mode. Opens http://localhost:3000

**To integrate the FRONTEND with BACKEND do following steps:**
 Enable CORS (Cross-Origin Resource Sharing) in FastAPI:  in main.py make sure to implement this (already implemented in the code and uploaded visit main.py in BACKEND folder)
 
         from fastapi.middleware.cors import CORSMiddleware 
         app.add_middleware(
              CORSMiddleware,
              allow_origins=["http://localhost:3000"],  # Frontend URL
              allow_credentials=True,
              allow_methods=["*"],
              allow_headers=["*"],
          )
   
**Running the Application :**
 1. Make sure the backend server is running at http://127.0.0.1:8000.
 2. Start the frontend server at http://localhost:3000.
 3. Open a web browser and go to http://localhost:3000 to use the Multi-Purpose ChatBot.

**Usage :**
 1. Visit the frontend URL http://localhost:3000 in your browser.
 2. Start a conversation with the ChatBot.
 3. Use the commands provided (e.g., web scraping, LinkedIn profile fetching).

   

