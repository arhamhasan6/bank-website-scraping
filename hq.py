from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re
import spacy
from collections import Counter
import sel 

def get_google_search_results(link):
    """
    Perform a Google search for the provided link to find the headquarters address.
    
    Args:
        link (str): The search query related to the headquarters address.
        
    Returns:
        list: A list of URLs obtained from the search results.
    """
    try:
        urls = []
        results = search(f"Head quarter address of {link}, only give me link from the provided website ")
        
        for i, result in enumerate(results):
            if i >= 2:
                break
            urls.append(result)
        
        return urls
    except Exception as e:
        return [f"Error: {e}"]


def clean_text(text):
    """
    Clean the given text by removing extra whitespace and joining parts into a single string.
    
    Args:
        text (str or tuple): The text to be cleaned.
        
    Returns:
        str: The cleaned text.
    """
    try:
        # Join the tuple into a single string if necessary
        text = ''.join(text) if isinstance(text, tuple) else text
        
        # Replace multiple whitespace (including newlines, tabs) with a single space
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading and trailing whitespace from the entire text
        text = text.strip()
        
        return text
    except Exception as e:
        print(f"Error in cleaning text: {e}")
        return ""


def find_addresses_in_text(text):
    """
    Extract addresses from the provided text using named entity recognition.
    
    Args:
        text (str): The text to search for addresses.
        
    Returns:
        list: A list of addresses found in the text.
    """
    try:
        # Load NLP model
        nlp = spacy.load("en_core_web_md")
        all_addresses = []
        doc = nlp(text)
        
        for ent in doc.ents:
            if ent.label_ in ("GPE"):
                all_addresses.append(ent.text)
        
        return all_addresses
    except Exception as e:
        print(f"Error in finding addresses: {e}")
        return []


def get_location(resp):
    """
    Extract relevant location information from the HTML content of a webpage.
    
    Args:
        resp (str): The HTML content of the webpage.
        
    Returns:
        list or str: Relevant sections containing location information or a message if none found.
    """
    try:
        # Parse the HTML content
        soup = BeautifulSoup(resp, 'html.parser')
        
        # Define keywords to search for
        keywords = ['headquarters','address','head office', 'principal office','headquartered']
        relevant_sections = []
        seen_texts = set() 
        
        # Search through various tags and their text content
        tags_to_check = ['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        
        for tag in tags_to_check:
            elements = soup.find_all(tag)
            for element in elements:
                text = element.get_text(separator=' ').strip()
                normalized_text = text.lower()
                if  any(keyword in normalized_text for keyword in keywords):
                    if normalized_text not in seen_texts:
                        relevant_sections.append({
                            'tag': tag,
                            'text': text
                        })
                        seen_texts.add(normalized_text)
        
        return relevant_sections if relevant_sections else 'No relevant sections found'
    except Exception as e:
        print(f"Error in extracting location: {e}")
        return 'Error extracting location'


def find_hq_address(url):
    """
    Find the headquarters address from the given URL by fetching and processing the webpage.
    
    Args:
        url (str): The URL of the webpage to fetch and process.
        
    Returns:
        list or str: A list of relevant sections containing headquarters address or a message if none found.
    """
    try:
        # Fetch the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return get_location(response.content)
    except requests.exceptions.RequestException as e:
        # Handle the exception and call the alternative method
        print(f"Error occurred while fetching the webpage: {e}")
        try:
            data = sel.selenium_get_data(url)
            return get_location(data)
        except Exception as e:
            print(f"Error in alternative method: {e}")
            return 'Error finding headquarters address'


def hq_loc(website_url: str) -> str:
    """
    Process the URL to find and return the headquarters location.
    
    Args:
        url (str): The URL to process.
        
    Returns:
        str: The most common headquarters location or a message if none found.
    """
    try:
        urls = get_google_search_results(website_url)
        results = find_hq_address(urls[0])

        if isinstance(results, list):
            location_list = []
            for result in results:
                location_list.extend(find_addresses_in_text(result['text']))

            # Count the frequency of each word
            word_counts = Counter(location_list)
            # Find the most common word
            most_common_word, _ = word_counts.most_common(1)[0]
            return most_common_word

        else:
            return "no location found"
    except Exception as e:
        print(f"Error in processing headquarters location: {e}")
        return "Error processing headquarters location"


# hq_loc( "https://www.usbank.com/")