import re
import math
from collections import defaultdict
from database import init_db, save_pages, save_index
from crawler import load_data

def build_index(page_content):
    inverted_index = defaultdict(list)
    tf_scores = {}
    total_docs = len(page_content)

    for url, content in page_content.items():
        words = re.findall(r'\b[a-z]{3,}\b', content.lower())
        total_words = len(words)
        word_count = defaultdict(int)

        for word in words:
            word_count[word] += 1

        tf_scores[url] = {
            word: count / total_words 
            for word, count in word_count.items()
        }

        for word in set(words):
            inverted_index[word].append(url)

    idf_scores = {}
    for word, urls in inverted_index.items():
        idf_scores[word] = math.log(total_docs / len(urls))

    return dict(inverted_index), tf_scores, idf_scores

if __name__ == "__main__":
    init_db()
    print("Loading crawled data...")
    _, page_content = load_data()
    
    print("Saving pages to database...")
    save_pages(page_content)
    
    print("Building index...")
    index, tf_scores, idf_scores = build_index(page_content)
    
    print("Saving index to database...")
    save_index(index, tf_scores, idf_scores)
    print(f"Done - {len(index)} unique words indexed")