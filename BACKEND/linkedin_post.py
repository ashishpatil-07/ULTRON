import os
import requests
from dotenv import load_dotenv
load_dotenv()
profile_id = os.getenv('LINKEDIN_PROFILE_ID_URN')

def post_update(LINKEDIN_ACCESS_TOKEN, message, image_paths=None):
    """
    Post an update on LinkedIn with multiple images and multi-line captions.
    Parameters:
        LINKEDIN_ACCESS_TOKEN (str): The LinkedIn access token for authentication.
        message (str): The message to post as an update.
        image_paths (list, optional): List of paths to image files to upload.
    Returns:
        dict: A dictionary containing the response from LinkedIn or an error message.
    """
    if not profile_id:
        return {"error": "Profile ID not found in .env file."}
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        "author": f"urn:li:person:{profile_id}",
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
    if image_paths and len(image_paths) > 0:
        # Upload all images and collect their URNs
        media_list = []
        for index, image_path in enumerate(image_paths):
            image_urn = upload_image_to_linkedin(LINKEDIN_ACCESS_TOKEN, image_path)
            if "error" in image_urn:
                return image_urn  # Return error if any image upload fails
            media_list.append({
                "status": "READY",
                "description": {
                    "text": f"Image {index + 1} uploaded via JARVIS"
                },
                "media": image_urn,
                "title": {
                    "text": os.path.basename(image_path)
                }
            })
        # Update payload to include multiple images
        payload["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
        payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = media_list
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        if image_paths:
            for image_path in image_paths:
                try:
                    os.remove(image_path)
                except:
                    pass  
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
            "owner": f"urn:li:person:{profile_id}",
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
        with open(image_path, 'rb') as image_file:
            upload_response = requests.put(upload_url, data=image_file, headers={'Authorization': f'Bearer {access_token}'})
            upload_response.raise_for_status()
        return asset
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to upload image: {str(e)}"}
