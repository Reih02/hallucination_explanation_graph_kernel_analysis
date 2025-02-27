from wikidata.client import Client
from LLM_wb import *
import wikipedia
import requests
from bs4 import BeautifulSoup
import time
# import concurrent.futures

# def process_text_in_parallel(text, chunk_size=500):
#     text_chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
#     relations_results = []
    
#     with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#         futures = {executor.submit(construct_kgs, chunk): chunk for chunk in text_chunks}
#         for future in concurrent.futures.as_completed(futures):
#             result = future.result()
#             if result and "relations" in result:
#                 relations_results.extend(result["relations"])
    
#     return relations_results


def find_url(entity):
    client = Client()
    entity = client.get(entity, load=True)

    url = entity.data['sitelinks']['enwiki']['url']

    return url

def get_wikipedia_url(search_string):
    try:
        page = wikipedia.page(search_string)
        return page.url
    except wikipedia.exceptions.DisambiguationError as e:
        return wikipedia.page(e.options[0]).url
    except wikipedia.exceptions.PageError:
        return None

def scrape_wikipedia_text(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page with status code: {response.status_code}")
    soup = BeautifulSoup(response.content, 'html.parser')
    content_div = soup.find('div', id='mw-content-text')

    if content_div is None:
        raise Exception("Could not find the main content on the page.")
    paragraphs = content_div.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])

    return text

def find_wikipedia_info_entity_link(entity):
    try:
        url_wikidata = find_url(entity)
        text_wikidata = scrape_wikipedia_text(url_wikidata)
        #relations = construct_kgs(text_wikidata)['relations']  
        relations = construct_kgs(text_wikidata)['relations']
    except:
        return None
    return relations

def find_wikipedia_info_search(entity):
    try:
        url_search = get_wikipedia_url(entity)
        text_search = scrape_wikipedia_text(url_search)
        relations = construct_kgs(text_search)['relations']
        return relations
    except:
        return None




# # Example usage
# search_string = "neurologist"
# url = get_wikipedia_url(search_string)
# if url:
#     print(f"Wikipedia URL for '{search_string}': {url}")
# else:
#     print(f"No Wikipedia page found for '{search_string}'.")
