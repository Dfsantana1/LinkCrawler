import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def scrape_data(url, follow_links):
    data = {}
    data[url] = get_text_from_url(url)
    
    if follow_links:
        links = get_links_from_url(url)
        for link in links:
            data[link] = get_text_from_url(link)
    return data

def get_text_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"There was an error trying to access {url}: Status code {response.status_code}")
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except requests.exceptions.RequestException as e:
        print(f"There was an error trying to access {url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain

def get_links_from_url(url):
    domain = get_domain(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith(domain)]
    return links

url = input("Please enter a URL: ")
follow_links = input("Do you want to follow the links? (True/False): ")

follow_links = follow_links.lower() == 'true'
print(f"URL: {url}\nFollow Links: {follow_links}\n")

print("Starting the scraping process...")
data = scrape_data(url, follow_links)
for url, text in data.items():
    print(f"URL: {url}\nText: {text}\n")
