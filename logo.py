import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sel
from selenium.webdriver.common.by import By
import time


def get_logo(website_url, resp):
    """
    Find the logo URL from the HTML content of the given website.

    Args:
        website_url (str): The base URL of the website to resolve relative paths.
        resp (str): The HTML content of the webpage.

    Returns:
        str: The absolute URL of the logo if found, or None if not found.
    """
    try:
        headers = {
            'User-agent': 'your bot 0.1'
        }

        soup = BeautifulSoup(resp, 'html.parser')

        # Function to ensure URLs are absolute
        def ensure_absolute_url(url):
            return urljoin(website_url, url)

        # Try to find the logo in common places
        logo = None
        
        # Check for <link rel="icon" ...> or <link rel="shortcut icon" ...>
        logo = soup.find('link', rel=lambda value: value and 'icon' in value.lower())
        if logo and 'href' in logo.attrs:
            return ensure_absolute_url(logo['href'])
        
        # Check for <img> tags with keywords in their 'alt' or 'class' attributes
        for img in soup.find_all('img'):
            alt = img.get('alt', '').lower()
            class_name = img.get('class', [])
            if 'logo' in alt or 'logo' in ' '.join(class_name).lower():
                return ensure_absolute_url(img['src'])

        # Check for common logo filenames in case the above logic fails
        common_logo_filenames = ['logo.png', 'logo.jpg', 'logo.gif', 'logo.svg']
        for filename in common_logo_filenames:
            potential_logo_url = ensure_absolute_url(filename)
            try:
                logo_response = requests.head(potential_logo_url, headers=headers)
                if logo_response.status_code == 200:
                    return potential_logo_url
            except requests.RequestException as e:
                print(f"Error checking logo URL {potential_logo_url}: {e}")

    except Exception as e:
        print(f"Error in get_logo function: {e}")
        return None


def find_logos(website_url: str) -> str:
    """
    Find the logo URL for the given website.

    Args:
        website_url (str): The URL of the website to fetch and process.

    Returns:
        str: The URL of the logo if found, or an error message if not found.
    """
    try:
        # Fetch the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(website_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return get_logo(website_url, response.content)
    
    except requests.exceptions.RequestException as e:
        # Handle the exception and call the alternative method
        print(f"Error occurred while fetching the webpage: {e}")
        try:
            return sel.logo_url(website_url)
        except Exception as e:
            print(f"Error in alternative method for finding logo: {e}")
            return "Error finding logo"



# # Example usage:
# website_url = "https://www.meezanbank.com/"
# logo_url = find_logos(website_url)
# print(logo_url)
