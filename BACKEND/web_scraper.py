import requests
from bs4 import BeautifulSoup
import logging
logging.basicConfig(level=logging.INFO)
def scrape_website(url: str, text_to_find: str) -> dict:
    """ Function to scrape a webpage and search for specific text within readable content."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful (200 OK)
        soup = BeautifulSoup(response.content, 'html.parser')
        for unwanted in soup(['script', 'style', 'meta', 'header', 'footer', 'link']):
            unwanted.decompose()  # Remove the unwanted tags from the content
        matched_elements = soup.find_all(string=lambda text: text_to_find.lower() in text.lower())
        occurrences = len(matched_elements)  # Count how many times the text appears
        examples = [
            element.find_parent().get_text(strip=True) 
            for element in matched_elements
        ][:10]  # Limit to the first 10 examples
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
