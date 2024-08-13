from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import urljoin
import re

def selenium_get_data(url):
    """
    Fetch the HTML source code of a webpage using Selenium.

    Parameters:
        url (str): The URL of the website to fetch data from.

    Returns:
        str: The page source as a string, or an error message if an issue occurs.
    """
    driver = None  # Initialize driver variable
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')

        # Initialize undetected Chrome driver
        try:
            driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        except Exception as e:
            return f"Error initializing the Chrome driver: {e}"

        # Try to open the website
        try:
            driver.get(url)
        except Exception as e:
            return f"Error loading the URL: {e}"

        # Wait until the body tag is loaded
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except Exception as e:
            return f"Error waiting for the page to load: {e}"

        # Get the page source
        try:
            page_source = driver.page_source
        except Exception as e:
            return f"Error retrieving the page source: {e}"

        # Add a delay before closing the browser
        time.sleep(5)

        return page_source

    except Exception as e:
        return f"An unexpected error occurred: {e}"

    finally:
        if driver:
            try:
                driver.close()  # Ensure the driver is closed
            except Exception as e:
                print(f"Error during driver.quit(): {e}")


def logo_url(url):
    """
    Extract the URL of a website's logo.

    Parameters:
        url (str): The URL of the website to extract the logo from.

    Returns:
        str: The URL of the logo or a message indicating no valid logo was found.
    """
    driver = None
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')

        # Initialize undetected Chrome driver
        driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Try to open the website
        try:
            driver.get(url)
        except Exception as e:
            return f"Error loading the URL: {e}"

        # Wait until the body tag is loaded
        try:
            WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except Exception as e:
            return f"Error waiting for the page to load: {e}"

        # Function to ensure URLs are absolute
        def ensure_absolute_url(url, base_url):
            return urljoin(base_url, url)

        # Try to find the logo in common places
        logo_url = None

        # Check for <link rel="icon" ...> or <link rel="shortcut icon" ...>
        try:
            icon_link = driver.find_element(By.XPATH, "//link[contains(@rel, 'icon')]")
            if icon_link:
                logo_url = ensure_absolute_url(icon_link.get_attribute("href"), url)
        except Exception as e:
            print(f"Error finding icon link: {e}")

        # Check for <img> tags with keywords in their 'alt' or 'class' attributes
        if not logo_url:
            try:
                logo_img = driver.find_element(By.XPATH, "//img[contains(@alt, 'logo') or contains(@class, 'logo')]")
                if logo_img:
                    logo_url = ensure_absolute_url(logo_img.get_attribute("src"), url)
            except Exception as e:
                print(f"Error finding logo image: {e}")

        # Check for common logo filenames in case the above logic fails
        if not logo_url:
            common_logo_filenames = ['logo.png', 'logo.jpg', 'logo.gif', 'logo.svg']
            for filename in common_logo_filenames:
                potential_logo_url = ensure_absolute_url(filename, url)
                try:
                    driver.get(potential_logo_url)
                    if driver.current_url == potential_logo_url and driver.title:
                        logo_url = potential_logo_url
                        break
                except Exception as e:
                    print(f"Error checking common logo filename: {e}")

        # Add a delay before closing the browser
        time.sleep(10)

        # Return the logo URL or a message if not found
        return logo_url if logo_url else "No valid logo found"

    except Exception as e:
        return f"An unexpected error occurred: {e}"

    finally:
        if driver:
            try:
                driver.quit()  # Ensure the driver is closed
            except Exception as e:
                print(f"Error during driver.quit(): {e}")


def clean_text(text):
    """
    Clean up a text string by removing excessive whitespace.

    Parameters:
        text (str): The text string to clean.

    Returns:
        str: The cleaned text string.
    """
    # Replace multiple whitespace (including newlines, tabs) with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading and trailing whitespace from the entire text
    text = text.strip()
    
    return text


def find_keywords_in_page_source(driver, keywords):
    """
    Search for specific keywords in the page source and return relevant sections.

    Parameters:
        driver (webdriver): The Selenium WebDriver instance.
        keywords (list): A list of keywords to search for.

    Returns:
        list: A list of dictionaries containing tag and text of relevant sections.
    """
    relevant_sections = []
    seen_texts = set()
    
    # Define tags to check (you can adjust this list as needed)
    tags_to_check = ['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

    # Search through various tags and their text content
    for tag in tags_to_check:
        try:
            elements = driver.find_elements(By.TAG_NAME, tag)
            for element in elements:
                text = element.text.strip()
                normalized_text = clean_text(text.lower())
                
                if 10 < len(normalized_text) < 600:
                    for keyword in keywords:
                        pattern = r'\b' + re.escape(keyword) + r'\b'
                        if re.search(pattern, normalized_text):
                            if normalized_text not in seen_texts:
                                relevant_sections.append({
                                    'tag': tag,
                                    'text': text
                                })
                                seen_texts.add(normalized_text)
                            break  # Stop checking further keywords once a match is found
        except Exception as e:
            print(f"Error processing tag {tag}: {e}")

    return relevant_sections


def selenium_get_dat(url, keywords):
    """
    Extract relevant sections of a webpage based on specified keywords.

    Parameters:
        url (str): The URL of the website to fetch data from.
        keywords (list): A list of keywords to search for.

    Returns:
        list: A list of relevant sections containing the specified keywords, or an error message.
    """
    driver = None  # Initialize driver as None
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')

        # Initialize undetected Chrome driver
        driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Try to open the website
        try:
            driver.get(url)
        except Exception as e:
            return f"Error loading the URL: {e}"

        # Wait until the body tag is loaded
        try:
            WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except Exception as e:
            return f"Error waiting for the page to load: {e}"

        # Extract relevant sections based on keywords
        relevant_sections = find_keywords_in_page_source(driver, keywords)

        return relevant_sections

    except Exception as e:
        return f"Error: {e}"

    finally:
        # Ensure the browser is closed if an error occurs or after the processing is done
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error during driver.quit(): {e}")


def mission_data(url):
    """
    Extract sections of a webpage related to 'mission', 'purpose', and 'success'.

    Parameters:
        url (str): The URL of the website to analyze.

    Returns:
        list: A list of relevant sections related to mission keywords.
    """
    keywords = ['mission', 'purpose', 'success']
    return selenium_get_dat(url, keywords)


def vision_data(url):
    """
    Extract sections of a webpage related to 'vision', 'ambition', 'future', and 'standards'.

      Parameters:
        url (str): The URL of the website to analyze.

    Returns:
        list: A list of relevant sections related to mission keywords.
    """
    keywords = ['vision', 'ambition', 'future', 'standards']
    return selenium_get_dat(url,keywords)


