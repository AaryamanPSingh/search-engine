import json
import re
from collections import defaultdict

def build_index(page_content):
    inverted_index = defaultdict(list)  # word -> list of urls
    
    for url, content in page_content.items():
        # Clean and tokenize text
        words = re.findall(r'\b[a-z]{3,}\b', content.lower())
        # Remove duplicates for this page
        unique_words = set(words)
        
        for word in unique_words:
            inverted_index[word].append(url)
    
    return dict(inverted_index)

def save_index(index, filename='index.json'):
    with open(filename, 'w') as f:
        json.dump(index, f)
    print(f"Index built with {len(index)} unique words")

def load_index(filename='index.json'):
    with open(filename, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    from crawler import load_data
    
    print("Loading crawled data...")
    link_graph, page_content = load_data()
    
    print("Building index...")
    index = build_index(page_content)
    save_index(index)