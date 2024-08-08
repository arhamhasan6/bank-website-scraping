# bank-website-scraping
## Website Logo Scraper

This Python script scrapes a given website to find and return the URL of the website's logo. The script uses the `requests` library to fetch the website's content and `BeautifulSoup` from the `bs4` library to parse the HTML and locate the logo.

## Features

- Scrapes a given website to find the logo URL.
- Searches for the logo in common locations, such as:
  - `<link rel="icon" ...>`
  - `<img>` tags with keywords in their 'alt' or 'class' attributes.
- Handles HTTP errors and exceptions gracefully.

## Prerequisites

Make sure you have the following Python libraries installed:

- `requests`
- `beautifulsoup4`

You can install them using `pip`:
To run the api start with the following command :
```sh
uvicorn main:app --reload
