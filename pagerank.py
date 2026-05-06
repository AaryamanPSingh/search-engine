import numpy as np
import json

def compute_pagerank(link_graph, damping=0.85, max_iterations=100, tolerance=1e-6):
    pages = list(link_graph.keys())
    n = len(pages)
    page_index = {page: i for i, page in enumerate(pages)}
    
    # Build adjacency matrix
    adjacency = np.zeros((n, n))
    for page, links in link_graph.items():
        i = page_index[page]
        valid_links = [l for l in links if l in page_index]
        if valid_links:
            for link in valid_links:
                j = page_index[link]
                adjacency[j][i] = 1.0 / len(valid_links)
        else:
            # Dangling node — distribute equally to all pages
            adjacency[:, i] = 1.0 / n

    # PageRank matrix with damping factor
    pagerank_matrix = damping * adjacency + (1 - damping) / n * np.ones((n, n))

    # Power iteration
    ranks = np.ones(n) / n
    for iteration in range(max_iterations):
        new_ranks = pagerank_matrix @ ranks
        if np.linalg.norm(new_ranks - ranks) < tolerance:
            print(f"Converged after {iteration + 1} iterations")
            break
        ranks = new_ranks

    return {pages[i]: ranks[i] for i in range(n)}

def save_pagerank(ranks, filename='pagerank.json'):
    with open(filename, 'w') as f:
        json.dump(ranks, f)
    print(f"PageRank computed for {len(ranks)} pages")

def load_pagerank(filename='pagerank.json'):
    with open(filename, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    from crawler import load_data
    
    print("Loading link graph...")
    link_graph, _ = load_data()
    
    print("Computing PageRank...")
    ranks = compute_pagerank(link_graph)
    save_pagerank(ranks)
    
    # Print top 10 pages
    top_pages = sorted(ranks.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\nTop 10 pages by PageRank:")
    for url, score in top_pages:
        print(f"{score:.6f} - {url}")