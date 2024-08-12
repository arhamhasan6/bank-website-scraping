import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
import sel
import bert_summarizer

def get_google_search_results(link,t):
    try:
        # Perform the search and collect the URLs
        urls = []
        results = search(f"mission statement of {link}, only give me link of the page where it exist in the provided website ")
        
        for i, result in enumerate(results):
            if i >= 2:
                break
            urls.append(result)
        
        return urls
    except Exception as e:
        return f"Error: {e}"
    

def clean_text(text):
    # Join the tuple into a single string
    text = ''.join(text)
    
    # Replace multiple whitespace (including newlines, tabs) with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading and trailing whitespace from the entire text
    text = text.strip()
    
    return text






def get_data(resp):
        # Parse the HTML content
        soup = BeautifulSoup(resp, 'html.parser')
        
        # Define keywords and patterns to search for mission
        keywords = ['mission','purpose','Innovative','dedicated']
      
        relevant_sections = []
        seen_texts = set() 
        # Search through various tags and their text content
        tags_to_check = ['p','div','span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        
        for tag in tags_to_check:
            elements = soup.find_all(tag)
           
            for element in elements:
                text = element.get_text(separator=' ').strip()
                normalized_text = clean_text(text.lower())

                if  15<len(normalized_text)<500 and any(keyword in normalized_text for keyword in keywords):
                                    if normalized_text not in seen_texts:
                                        relevant_sections.append({
                                            'tag': tag,
                                            'text': text
                                        })
                                        seen_texts.add(normalized_text)
        
        # Return relevant sections
        if relevant_sections:
            return relevant_sections
        else:
            return 'No relevant sections found'

    
def find_vision_mission_values(url):
    try:
        # Fetch the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return get_data(response.content)

    except requests.exceptions.RequestException as e:
        # Handle the exception and call the alternative method
        print(f"Error occurred while fetching the webpage: {e}")
        return sel.mission_data(url)



url_list=[
    "mission statement of "
]

# def process_urls(url,url_list=url_list):
#     j=""
#     urls = get_google_search_results(url, j)
#     results = find_vision_mission_values(urls[0])



#     if isinstance(results, list):
#         print("Relevant Sections:")
#         for result in results:
#             all_text += clean_text(result['text']) + " "  # Add a space between texts for readability
                  
#         return all_text.strip()

#     else:
#         pass

found_result = False

def process_urls(url,url_list=url_list):
    all_text = ""
    found = False

    for j in url_list:
        urls = get_google_search_results(url, j)
        print(urls)
        
        for i in urls:
            results = find_vision_mission_values(i)
            
            if results:
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
# Return the collected text immediately when found

    # If no data is found after all loops
    if not found:
        return "mission statement not found"
# # # Call the function
# process_urls('https://www.db.com/profile')