


import requests
from bs4 import BeautifulSoup

def get_logo_url(website_url: str) -> str:
    try:
        # Headers to simulate a browser visit
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the content of the website
        response = requests.get(website_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Try to find the logo in common places
        logo = None
        # Check for <link rel="icon" ...>
        logo = soup.find('link', rel=lambda value: value and 'icon' in value.lower())
        if logo:
            return logo['href']
        
        # Check for <img> tags with keywords in their 'alt' or 'class' attributes
        for img in soup.find_all('img'):
            alt = img.get('alt', '').lower()
            class_name = img.get('class', [])
            if 'logo' in alt or 'logo' in class_name:
                return img['src']
        
        # If no logo found
        return 'No valid logo found'
    except Exception as e:
        return f"Error: {e}"

