from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import aiofiles
from dotenv import load_dotenv
import google.generativeai as ai
import requests
from web_scraper import scrape_website
from linkedin_post import post_update
from typing import List, Dict, Any

app = FastAPI()

# Set up CORS to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
load_dotenv()

key = os.getenv('GEMINI_API_KEY')
LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')

# Configure Google Generative AI
ai.configure(api_key=key)
model = ai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

# Global variable to store the last scraping result
last_scraping_result: Dict[str, Any] = {}

# Define the data models
class ScrapeRequest(BaseModel):
    url: str
    text_to_find: str

class LinkedInPostRequest(BaseModel):
    message: str

class ChatRequest(BaseModel):
    message: str

# Route to scrape a website
@app.post("/scrape")
async def scrape_endpoint(request: ScrapeRequest):
    global last_scraping_result  # Use the global variable to store results
    try:
        result = scrape_website(request.url, request.text_to_find)
        last_scraping_result = {
            "occurrences": result['occurrences'],
            "examples": result['examples']
        } 
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping website: {str(e)}")

@app.post("/linkedin/image-upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        os.makedirs("uploads", exist_ok=True)
        
        # Save the uploaded file
        file_path = f"uploads/{file.filename}"
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        return {"message": f"Image {file.filename} uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")


@app.post("/linkedin/post")
async def linkedin_post_endpoint(
    message: str = Form(...),
    images: List[UploadFile] = File(default=None)
    ):
    try:
        image_paths = []
        if images:
            # Create uploads directory if it doesn't exist
            os.makedirs("uploads", exist_ok=True)
            
            # Save all uploaded images
            for image in images:
                # Generate a unique filename to avoid conflicts
                unique_filename = f"{os.urandom(8).hex()}_{image.filename}"
                image_path = f"uploads/{unique_filename}"
                
                # Save the file
                async with aiofiles.open(image_path, 'wb') as out_file:
                    content = await image.read()
                    await out_file.write(content)
                image_paths.append(image_path)
        
        # Post to LinkedIn with message and any images
        response = post_update(LINKEDIN_ACCESS_TOKEN, message, image_paths)
        
        # Check for errors in the response
        if "error" in response:
            raise HTTPException(status_code=500, detail=str(response["error"]))
            
        return {
            "message": "Successfully posted to LinkedIn",
            "response": response
        }
    except Exception as e:
        # Clean up any uploaded files in case of error
        for path in image_paths:
            try:
                os.remove(path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Error posting to LinkedIn: {str(e)}")

# Route to send a message to Google Generative AI chat
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    global last_scraping_result  # Use the global variable for scraping results
    try:
        user_message = request.message.lower()

        # Check if the user is asking about the scraping results
        if "occurrences" in user_message:
            response_text = f"I found {last_scraping_result.get('occurrences', 0)} occurrences of the text you searched for."
        elif "examples" in user_message:
            examples = last_scraping_result.get('examples', [])
            response_text = "Here are some examples:\n" + "\n".join(examples) if examples else "No examples found."
        else:
            # For other messages, send to the AI model
            response = chat.send_message(request.message)
            response_text = response.text

        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending message to chat model: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
