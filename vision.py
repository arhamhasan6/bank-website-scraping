import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
import sel
from typing import List, Dict, Union
import bert_summarizer


def get_google_search_results(link: str, search_text: str) -> List[str]:
    """
    Perform a Google search for the specified term and URL, and return a list of up to 2 URLs.

    Args:
        link (str): The base URL of the website to search within.
        t (str): The search term to include in the query.

    Returns:
        List[str]: A list of up to 2 URLs where the term is mentioned.
    """
    try:
        urls = []
        results = search(f"{search_text} {link}, only give me link of the page where it exist in the provided website")
        
        for i, result in enumerate(results):
            if i >= 2:
                break
            urls.append(result)
        
        return urls
    except Exception as e:
        print(f"Error occurred in get_google_search_results: {e}")
        return []


def clean_text(text: str) -> str:
    """
    Clean the input text by joining tuples into a single string, replacing multiple whitespace with a single space,
    and stripping leading and trailing whitespace.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.
    """
    try:
        text = ''.join(text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    except Exception as e:
        print(f"Error occurred in clean_text: {e}")
        return ""


def get_data(resp: bytes) -> Union[List[Dict[str, str]], str]:
    """
    Extract relevant sections of text from the HTML content based on predefined keywords.

    Args:
        resp (bytes): The HTML content of the webpage.

    Returns:
        Union[List[Dict[str, str]], str]: A list of dictionaries containing relevant sections of text,
                                           or a message indicating no relevant sections were found.
    """
    try:
        soup = BeautifulSoup(resp, 'html.parser')
        
        keywords = ['vision', 'ambition', 'committed','future of banking.','standards']
        relevant_sections = []
        seen_texts = set()
        tags_to_check = ['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        
        for tag in tags_to_check:
            elements = soup.find_all(tag)
            for element in elements:
                text = element.get_text(separator=' ').strip()
                normalized_text = clean_text(text.lower())
                
                if 15 < len(normalized_text) < 500:
                    for keyword in keywords:
                        pattern = r'\b' + re.escape(keyword) + r'\b'
                        if re.search(pattern, normalized_text):
                            if normalized_text not in seen_texts:
                                relevant_sections.append({
                                    'tag': tag,
                                    'text': text
                                })
                                seen_texts.add(normalized_text)
        
        if relevant_sections:
            return relevant_sections
        else:
            return 'No relevant sections found'
    except Exception as e:
        print(f"Error occurred in get_data: {e}")
        return 'Error processing content'


def find_vision_mission_values(url: str) -> Union[List[Dict[str, str]], str]:
    """
    Fetch the webpage content and extract vision and mission values.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        Union[List[Dict[str, str]], str]: A list of dictionaries containing vision and mission values,
                                           or an error message if the request fails.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return get_data(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching the webpage: {e}")
        try:
            return sel.vision_data(url)
        except Exception as e:
            print(f"Error in alternative method for vision data: {e}")
            return 'Error fetching vision data'


url_list = [
    "vision statement of ",
    "diversity of"
]


def process_urls(url: str, url_list: List[str] = url_list) -> str:
    """
    Process a list of search terms to find and extract vision and mission statements from the URLs.

    Args:
        url (str): The base URL to search within.
        url_list (List[str], optional): A list of search terms. Defaults to url_list.

    Returns:
        str: The collected text of vision and mission statements or a message indicating no data was found.
    """
    try:
        all_text = ""
        found = False

        for j in url_list:
            urls = get_google_search_results(url, j)
            print(urls)
            
            for i in urls:
                results = find_vision_mission_values(i)
                
                if isinstance(results, list):
                    # if len(results)>1:
                    #     for result in results:
                    #         all_text += clean_text(result['text']) + " "
                    #         found = True  # Set found to True as soon as any relevant text is found
                        
                    #     if found:
                    #         summary = bert_summarizer.text_summarizer_from_pdf(all_text.strip() )
                    #         return summary  # Return the collected text immediately when found
                    # else:
                        for result in results:
                            all_text += clean_text(result['text']) + " "
                            found = True  # Set found to True as soon as any relevant text is found
                        
                        if found:
                            return all_text.strip()  # Return the collected text immediately when found

        
        if not found:
            return "Vision statement not found"
    except Exception as e:
        print(f"Error occurred in process_urls: {e}")
        return "Error processing URLs"
                        
# # # Call the function
# process_urls('https://www.db.com/profile')


        
       
        

