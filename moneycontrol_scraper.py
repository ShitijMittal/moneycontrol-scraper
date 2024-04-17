import requests
from bs4 import BeautifulSoup
import json
 
# Function to extract article body from a given URL
def extract_article_body(url):
    try:
        # Send HTTP GET request to the article URL
        article_response = requests.get(url)
       
        # Check if the request to the article URL was successful
        if article_response.status_code == 200:
            # Parse the HTML content of the article page
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
           
            # Find the element containing the article body (adjust as per HTML structure)
            article_body_element = article_soup.find('div', class_='content_wrapper arti-flow')
           
            # Extract and return the article body content as bullet points
            if article_body_element:
                # Split the article body text into sentences
                sentences = article_body_element.get_text().split('.')
                # Create bullet points from the sentences
                bullet_points = '\n'.join([f"• {sentence.strip()}" for sentence in sentences if sentence.strip()])
                return bullet_points
            else:
                return 'Article body element not found.'
        else:
            return f'Failed to retrieve article URL: {url}. Status code: {article_response.status_code}'
    except Exception as e:
        return f'Error extracting article body from URL: {url}. Error: {e}'
 
# URL of the website to scrape
url = 'https://www.moneycontrol.com/'
 
# Send an HTTP GET request to the website
response = requests.get(url)
 
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')
 
    # Find script tags containing JSON data
    script_tags = soup.find_all('script', type='application/ld+json')
 
    # Extract JSON data from script tags
    for script_tag in script_tags:
        json_data = script_tag.string
       
        # Parse JSON data to extract "name" and "url" information
        try:
            data = json.loads(json_data)
            if isinstance(data, dict) and '@type' in data and data['@type'] == 'ItemList' and 'itemListElement' in data:
                for item in data['itemListElement']:
                    if '@type' in item and item['@type'] == 'ListItem' and 'name' in item and 'url' in item:
                        print(f"Name: {item['name']}")
                       
                        # Extract article body from the URL and format as bullet points
                        article_body = extract_article_body(item['url'])
                        print(f"Article Body:\n{article_body}\n")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON data: {e}")
 
else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)
 
