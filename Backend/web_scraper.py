import requests
from bs4 import BeautifulSoup
import logging

# Configure logging to show information for debugging purposes
logging.basicConfig(level=logging.INFO)

def scrape_website(url: str, text_to_find: str) -> dict:
    """
    Function to scrape a webpage and search for specific text within readable content.

    Args:
        url (str): URL of the webpage to scrape.
        text_to_find (str): The text you are searching for in the webpage.

    Returns:
        dict: Contains the count of text occurrences and a list of examples (full lines) or an error message if something goes wrong.
    """
    try:
        # Request the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful (200 OK)
        
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove tags that typically don't contain relevant text (scripts, styles, metadata)
        for unwanted in soup(['script', 'style', 'meta', 'header', 'footer', 'link']):
            unwanted.decompose()  # Remove the unwanted tags from the content

        # Search for the target text within readable text elements
        matched_elements = soup.find_all(string=lambda text: text_to_find.lower() in text.lower())
        occurrences = len(matched_elements)  # Count how many times the text appears

        # Extract the full text lines where the target text appears
        examples = [
            element.find_parent().get_text(strip=True)  # Extract full text from the parent element
            for element in matched_elements
        ][:10]  # Limit to the first 10 examples

        # Return the count of occurrences and some example lines
        return {
            'occurrences': occurrences,
            'examples': examples if examples else ['No examples found']
        }

    except requests.exceptions.RequestException as req_err:
        logging.error(f"Error while requesting the URL: {str(req_err)}")
        return {'error': f"Request error: {str(req_err)}"}
    
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return {'error': f"An unexpected error occurred: {str(e)}"}
