import json
from indexer import load_index
from pagerank import load_pagerank

def search(query, index, tf_scores, idf_scores, ranks, top_k=10):
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

    # Score = TF-IDF * PageRank
    results = []
    for page in matching_pages:
        tfidf_score = 0
        for word in words:
            tf = tf_scores.get(page, {}).get(word, 0)
            idf = idf_scores.get(word, 0)
            tfidf_score += tf * idf

        pagerank_score = ranks.get(page, 0)
        combined_score = tfidf_score * pagerank_score
        results.append((page, combined_score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]

def get_snippet(url, query, page_content, snippet_length=200):
    content = page_content.get(url, '')
    query_words = query.lower().split()
    
    # Clean content - remove short lines (navigation, menus)
    lines = content.split('\n')
    clean_lines = [line.strip() for line in lines if len(line.strip()) > 100]
    clean_content = ' '.join(clean_lines)
    
    # Clean up whitespace
    clean_content = ' '.join(clean_content.split())
    
    content_lower = clean_content.lower()
    best_pos = len(clean_content)
    
    for word in query_words:
        pos = content_lower.find(word)
        if pos != -1 and pos < best_pos:
            best_pos = pos
    
    if best_pos == len(clean_content):
        return clean_content[:snippet_length] + "..."
    
    start = max(0, best_pos - 50)
    end = min(len(clean_content), best_pos + snippet_length)
    snippet = clean_content[start:end].strip()
    
    return "..." + snippet + "..."

if __name__ == "__main__":
    print("Loading data...")
    index, tf_scores, idf_scores = load_index()
    ranks = load_pagerank()

    while True:
        query = input("\nSearch: ")
        if query == 'quit':
            break
        results = search(query, index, tf_scores, idf_scores, ranks)
        if results:
            print(f"\nTop results for '{query}':")
            for url, score in results:
                print(f"{score:.10f} - {url}")
        else:
            print("No results found")