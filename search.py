import json
from indexer import load_index
from crawler import load_data
from pagerank import load_pagerank

def search(query, index, ranks, top_k=10):
    words = query.lower().split()
    
    # Find pages containing all query words
    matching_pages = None
    for word in words:
        if word in index:
            pages = set(index[word])
            if matching_pages is None:
                matching_pages = pages
            else:
                matching_pages = matching_pages.intersection(pages)
        else:
            return []
    
    if not matching_pages:
        return []
    
    # Rank by PageRank score
    results = [(page, ranks.get(page, 0)) for page in matching_pages]
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results[:top_k]

if __name__ == "__main__":
    print("Loading data...")
    index = load_index()
    ranks = load_pagerank()
    
    while True:
        query = input("\nSearch: ")
        if query == 'quit':
            break
        results = search(query, index, ranks)
        if results:
            print(f"\nTop results for '{query}':")
            for url, score in results:
                print(f"{score:.10f} - {url}")
        else:
            print("No results found")