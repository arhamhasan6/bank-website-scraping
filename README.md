# Website Logo Scraper

This module extracts the logo URL from a website by parsing its HTML content.

## Functions

### `get_logo(website_url, resp)`

Searches for the website's logo within the HTML content.

- **Parameters**:
  - `website_url` (str): The base URL of the website.
  - `resp` (str): HTML content of the webpage.

- **Method**:
  1. Converts relative URLs to absolute.
  2. Looks for `<link>` tags with `rel="icon"`.
  3. Searches `<img>` tags with "logo" in the `alt` or `class` attributes.
  4. Checks common logo filenames (`logo.png`, `logo.jpg`, etc.).

- **Returns**: Absolute URL of the logo, if found.

### `find_logos(website_url: str) -> str`

Fetches the logo URL using `get_logo`.

- **Parameters**:
  - `website_url` (str): The URL of the website.

- **Method**:
  1. Sends an HTTP GET request to fetch the webpage.
  2. Handles errors and uses a fallback method if the request fails.

- **Returns**: The logo URL or a fallback value.
---

# Headquarters Location Scraper

This Python module is designed to find the headquarters address of a company by scraping relevant information from its website or search results.

## Functions

### `get_google_search_results(link)`

Searches Google for the headquarters address of a given company and returns URLs from the specified website.

- **Parameters**:
  - `link` (str): The base URL or name of the company.

- **Returns**: A list of URLs related to the headquarters address.

### `clean_text(text)`

Cleans and normalizes text by removing extra whitespace and formatting it into a single line.

- **Parameters**:
  - `text` (str): The text to be cleaned.

- **Returns**: Cleaned and normalized text.

### `find_addresses_in_text(text)`

Uses NLP to extract potential address-related entities from the provided text.

- **Parameters**:
  - `text` (str): The text from which to extract addresses.

- **Returns**: A list of addresses found in the text.

### `get_location(resp)`

Parses HTML content to find relevant sections containing keywords related to headquarters addresses.

- **Parameters**:
  - `resp` (str): The HTML content of the webpage.

- **Returns**: A list of relevant sections containing potential headquarters addresses.

### `find_hq_address(url)`

Fetches a webpage and attempts to find the headquarters address by searching through the content.

- **Parameters**:
  - `url` (str): The URL of the webpage.

- **Returns**: A list of sections with address-related information or a fallback if not found.

### `hq_loc(url)`

Combines all previous functions to search, fetch, and extract the most likely headquarters location for a given URL.

- **Parameters**:
  - `url` (str): The base URL or name of the company.

- **Returns**: The most common location name found, or a message if no location is found.

---

# Mission Statement Scraper

This Python module extracts mission statements from web pages by scraping content and searching for relevant keywords.

## Functions

### `get_google_search_results(link, t)`

Searches Google for mission statements of a given company or website and returns a list of URLs from the specified site.

- **Parameters**:
  - `link` (str): The base URL or name of the company.
  
- **Returns**: A list of URLs where mission statements may be found.

### `clean_text(text)`

Cleans and normalizes text by removing extra whitespace and joining multiple lines into a single string.

- **Parameters**:
  - `text` (str): The text to be cleaned.

- **Returns**: Cleaned and normalized text.

### `get_data(resp)`

Parses HTML content to extract sections related to mission statements based on predefined keywords.

- **Parameters**:
  - `resp` (str): The HTML content of the webpage.

- **Returns**: A list of relevant sections containing potential mission statements or 'No relevant sections found' if none are found.

### `find_vision_mission_values(url)`

Fetches the webpage from a given URL and attempts to extract mission statement sections.

- **Parameters**:
  - `url` (str): The URL of the webpage.

- **Returns**: A list of relevant sections containing potential mission statements or calls an alternative method if errors occur.

### `process_urls(url, url_list=url_list)`

Processes a list of URLs to find and return a consolidated string of mission statements.

- **Parameters**:
  - `url` (str): The base URL or name of the company.
  - `url_list` (list, optional): A list of additional search terms (default is an empty list).

- **Returns**: A single string containing all found mission statements or "mission statement not found" if no data is found.

---

# Vision Statement Scraper

This Python module extracts vision statements from web pages by scraping content and searching for relevant keywords.

## Functions

### `get_google_search_results(link, t)`

Searches Google for vision statements of a given company or website and returns a list of URLs from the specified site.

- **Parameters**:
  - `link` (str): The base URL or name of the company.
  - `t` (str): Additional search term related to vision statements.

- **Returns**: A list of URLs where vision statements may be found.

### `clean_text(text)`

Cleans and normalizes text by removing extra whitespace and joining multiple lines into a single string.

- **Parameters**:
  - `text` (str): The text to be cleaned.

- **Returns**: Cleaned and normalized text.

### `get_data(resp)`

Parses HTML content to extract sections related to vision statements based on predefined keywords.

- **Parameters**:
  - `resp` (str): The HTML content of the webpage.

- **Returns**: A list of relevant sections containing potential vision statements or 'No relevant sections found' if none are found.

### `find_vision_mission_values(url)`

Fetches the webpage from a given URL and attempts to extract vision statement sections.

- **Parameters**:
  - `url` (str): The URL of the webpage.

- **Returns**: A list of relevant sections containing potential vision statements or calls an alternative method if errors occur.

### `process_urls(url, url_list=url_list)`

Processes a list of URLs to find and return a consolidated string of vision statements.

- **Parameters**:
  - `url` (str): The base URL or name of the company.
  - `url_list` (list, optional): A list of additional search terms (default includes terms related to vision).

- **Returns**: A single string containing all found vision statements or "vision statement not found" if no data is found.

---

# FastAPI Web Scraper

This FastAPI application provides an endpoint to process a given URL and retrieve various data points related to the website, including its logo, headquarters, vision statement, and mission statement.

## Endpoints

### `POST /url`

Processes the provided URL to fetch and return various details.

**Request Body**:

- **website_url** (str): The URL of the website to process. Must be a valid HTTP or HTTPS URL.

**Response**:

- **logo** (str, optional): URL of the website's logo.
- **hq** (str, optional): Headquarters location extracted from the website.
- **vision** (str, optional): Vision statement extracted from the website.
- **mission** (str, optional): Mission statement extracted from the website.
- **logo_error** (str, optional): Error message if logo retrieval fails.
- **hq_error** (str, optional): Error message if retrieving headquarters fails.
- **vision_error** (str, optional): Error message if retrieving vision statement fails.
- **mission_error** (str, optional): Error message if retrieving mission statement fails.

**Errors**:

- **422 Unprocessable Entity**: Returned for invalid input or if any of the functions encounter an error.
- **500 Internal Server Error**: Returned for unexpected errors during request processing.

## Functionality

1. **Logo Retrieval**: Uses `logo.find_logos` to fetch the website's logo URL.
2. **Headquarters Location**: Uses `hq.hq_loc` to find the headquarters location.
3. **Vision Statement**: Uses `vision.process_urls` to extract the vision statement.
4. **Mission Statement**: Uses `mission.process_urls` to extract the mission statement.

---


To run the api start with the following command :
```sh
uvicorn main:app --reload

---
url:
http://127.0.0.1:8000/url


Input api with in the following format :

{
    "website_url":"https://www.cbd.ae/"
}
