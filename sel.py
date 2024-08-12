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

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')


    driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)

    # Wait until the body tag is loaded
    WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    ##############################################################################logo
    # # Function to ensure URLs are absolute
    def ensure_absolute_url(url, base_url):
        return urljoin(base_url, url)

    # Try to find the logo in common places
    logo_url = None

    # Check for <link rel="icon" ...> or <link rel="shortcut icon" ...>
    try:
        icon_link = driver.find_element(By.XPATH, "//link[contains(@rel, 'icon')]")
        if icon_link:
            logo_url = ensure_absolute_url(icon_link.get_attribute("href"), url)
    except:
        pass

    # Check for <img> tags with keywords in their 'alt' or 'class' attributes
    if not logo_url:
        try:
            logo_img = driver.find_element(By.XPATH, "//img[contains(@alt, 'logo') or contains(@class, 'logo')]")
            if logo_img:
                logo_url = ensure_absolute_url(logo_img.get_attribute("src"), url)
        except:
            pass

    # Check for common logo filenames in case the above logic fails
    if not logo_url:
        common_logo_filenames = ['logo.png', 'logo.jpg', 'logo.gif', 'logo.svg']
        for filename in common_logo_filenames:
            potential_logo_url = ensure_absolute_url(filename, url)
            driver.get(potential_logo_url)
            if driver.current_url == potential_logo_url and driver.title:
                logo_url = potential_logo_url
                break
    time.sleep(10)

    # Close the browser
    driver.quit()
    # Print the logo URL or a message if not found
    if logo_url:
        return logo_url
    else:
        return  "No valid logo found"

###################################################### vision ################################################################

def clean_text(text):
    # Replace multiple whitespace (including newlines, tabs) with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading and trailing whitespace from the entire text
    text = text.strip()
    
    return text

def find_keywords_in_page_source(driver,keywords):
    # Define keywords and patterns to search for
    relevant_sections = []
    seen_texts = set()
    
    # Define tags to check (you can adjust this list as needed)
    tags_to_check = ['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

    # Search through various tags and their text content
    for tag in tags_to_check:
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

    return relevant_sections

def selenium_get_dat(url,keywords):
    driver = None  # Initialize driver as None
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')

        # Initialize undetected Chrome driver
        driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Open the website
        driver.get(url)

        # Wait until the body tag is loaded
        WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Extract relevant sections based on keywords
        relevant_sections = find_keywords_in_page_source(driver,keywords)

        return relevant_sections

    except Exception as e:
        return f"Error: {e}"

    finally:
        # Ensure the browser is closed if an error occurs or after the processing is done
        if driver:
            driver.quit()



def mission_data(url):
    keywords = ['mission','purpose','success']
    return selenium_get_dat(url,keywords)

def vision_data(url):
    keywords = ['vision', 'ambition', 'future', 'standards']
    return selenium_get_dat(url,keywords)