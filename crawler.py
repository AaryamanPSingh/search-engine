import requests
from bs4 import BeautifulSoup
from collections import deque
import urllib.parse
import json

def crawl(seed_url, max_pages=500):
    visited = set()
    queue = deque([seed_url])
    link_graph = {}  # page -> list of pages it links to
    page_content = {}  # page -> raw text

    while queue and len(visited) < max_pages:
        url = queue.popleft()

        if url in visited:
            continue

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, timeout=5, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text
            page_content[url] = soup.get_text()

            # Extract links
            links = []
            for tag in soup.find_all('a', href=True):
                href = tag['href']
                # Convert relative URLs to absolute
                full_url = urllib.parse.urljoin(url, href)
                # Only keep Wikipedia math related pages
                if ('en.wikipedia.org/wiki' in full_url and 
                'Wikipedia:' not in full_url and
                'Help:' not in full_url and
                'Portal:' not in full_url and
                'Special:' not in full_url and
                'Talk:' not in full_url and
                'File:' not in full_url):
                    links.append(full_url)
                    if full_url not in visited:
                        queue.append(full_url)
            # After soup.find_all('a', href=True) loop, add:
            all_hrefs = [tag['href'] for tag in soup.find_all('a', href=True)]
            print(f"Total hrefs found: {len(all_hrefs)}")
            print(f"First 5: {all_hrefs[:5]}")
            link_graph[url] = links
            print(f"Found {len(links)} links on {url}")
        except:
            continue

        visited.add(url)
        print(f"Crawled {len(visited)}: {url}")

    return link_graph, page_content

def save_data(link_graph, page_content, graph_file='link_graph.json', content_file='page_content.json'):
    with open(graph_file, 'w') as f:
        json.dump(link_graph, f)
    with open(content_file, 'w') as f:
        json.dump(page_content, f)
    print("Data saved successfully")

def load_data(graph_file='link_graph.json', content_file='page_content.json'):
    with open(graph_file, 'r') as f:
        link_graph = json.load(f)
    with open(content_file, 'r') as f:
        page_content = json.load(f)
    return link_graph, page_content

if __name__ == "__main__":
    seed = "https://en.wikipedia.org/wiki/Mathematics"
    link_graph, page_content = crawl(seed, max_pages=500)
    print(f"Total pages crawled: {len(page_content)}")
    save_data(link_graph, page_content)