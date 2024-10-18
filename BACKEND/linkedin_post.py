import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
id = os.getenv('LINKEDIN_PROFILE_ID_URN') # Fetch the profile ID from environment variables

def post_update(LINKEDIN_ACCESS_TOKEN, message, image_paths=None):
    """
    Post an update on LinkedIn with optional multiple images.
    Parameters:
        LINKEDIN_ACCESS_TOKEN (str): The LinkedIn access token for authentication.
        message (str): The message to post as an update.
    Returns:
        dict: A dictionary containing the response from LinkedIn or an error message.
    """
    if not id:
        return {"error": "Profile ID not found in .env file."}
    
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        "author": f"urn:li:person:{id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    if image_paths:
        # If images are provided, we need to upload them first
        media_list = []
        for image_path in image_paths:
            image_urn = upload_image_to_linkedin(LINKEDIN_ACCESS_TOKEN, image_path)
            if "error" in image_urn:
                return image_urn  # Return the error if image upload failed
            media_list.append({
                "status": "READY",
                "description": {
                    "text": "Image uploaded via JARVIS"
                },
                "media": image_urn,
                "title": {
                    "text": os.path.basename(image_path)
                }
            })
        # Update the payload to include the images
        payload["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
        payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = media_list
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except ValueError:
        return {"error": "Failed to parse JSON response."}

def upload_image_to_linkedin(access_token, image_path):
    """
    Upload an image to LinkedIn.
    Parameters:
        access_token (str): The LinkedIn access token for authentication.
        image_path (str): The path to the image file to upload.

    Returns:
        str: The URN of the uploaded image or an error message.
    """
    register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    register_data = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": f"urn:li:person:{id}",
            "serviceRelationships": [{
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }]
        }
    }
    try:
        response = requests.post(register_url, headers=headers, json=register_data)
        response.raise_for_status()
        upload_url = response.json()['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        asset = response.json()['value']['asset']
        # Upload the image file
        with open(image_path, 'rb') as image_file:
            upload_response = requests.put(upload_url, data=image_file, headers={'Authorization': f'Bearer {access_token}'})
            upload_response.raise_for_status()
        return asset
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to upload image: {str(e)}"}
