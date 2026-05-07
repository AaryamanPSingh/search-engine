import numpy as np
from database import save_pagerank
from crawler import load_data

def compute_pagerank(link_graph, damping=0.85, max_iterations=100, tolerance=1e-6):
    pages = list(link_graph.keys())
    n = len(pages)
    page_index = {page: i for i, page in enumerate(pages)}
    
    adjacency = np.zeros((n, n))
    for page, links in link_graph.items():
        i = page_index[page]
        valid_links = [l for l in links if l in page_index]
        if valid_links:
            for link in valid_links:
                j = page_index[link]
                adjacency[j][i] = 1.0 / len(valid_links)
        else:
            adjacency[:, i] = 1.0 / n

    pagerank_matrix = damping * adjacency + (1 - damping) / n * np.ones((n, n))

    ranks = np.ones(n) / n
    for iteration in range(max_iterations):
        new_ranks = pagerank_matrix @ ranks
        if np.linalg.norm(new_ranks - ranks) < tolerance:
            print(f"Converged after {iteration + 1} iterations")
            break
        ranks = new_ranks

    return {pages[i]: float(ranks[i]) for i in range(n)}

if __name__ == "__main__":
    print("Loading link graph...")
    link_graph, _ = load_data()
    
    print("Computing PageRank...")
    ranks = compute_pagerank(link_graph)
    
    print("Saving to database...")
    save_pagerank(ranks)
    
    top_pages = sorted(ranks.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\nTop 10 pages by PageRank:")
    for url, score in top_pages:
        print(f"{score:.6f} - {url}")