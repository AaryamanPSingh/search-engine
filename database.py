import sqlite3
import json

def init_db():
    conn = sqlite3.connect('search_engine.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS pages
                 (url TEXT PRIMARY KEY, content TEXT, pagerank REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS index_table
                 (word TEXT, url TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS tfidf
                 (url TEXT, word TEXT, tf_score REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS idf_table
                 (word TEXT PRIMARY KEY, idf_score REAL)''')
    
    conn.commit()
    conn.close()

def save_pages(page_content):
    conn = sqlite3.connect('search_engine.db')
    c = conn.cursor()
    for url, content in page_content.items():
        c.execute('INSERT OR REPLACE INTO pages (url, content) VALUES (?, ?)', 
                  (url, content))
    conn.commit()
    conn.close()

def save_index(index, tf_scores, idf_scores):
    conn = sqlite3.connect('search_engine.db')
    c = conn.cursor()
    
    # Save inverted index
    for word, urls in index.items():
        for url in urls:
            c.execute('INSERT INTO index_table VALUES (?, ?)', (word, url))
    
    # Save TF scores
    for url, scores in tf_scores.items():
        for word, score in scores.items():
            c.execute('INSERT INTO tfidf VALUES (?, ?, ?)', (url, word, score))
    
    # Save IDF scores
    for word, score in idf_scores.items():
        c.execute('INSERT INTO idf_table VALUES (?, ?)', (word, score))
    
    conn.commit()
    conn.close()

def save_pagerank(ranks):
    conn = sqlite3.connect('search_engine.db')
    c = conn.cursor()
    count = 0
    for url, score in ranks.items():
        # First try to update existing row
        c.execute('UPDATE pages SET pagerank = ? WHERE url = ?', (score, url))
        if c.rowcount == 0:
            # Row doesn't exist, insert new one
            c.execute('INSERT INTO pages (url, pagerank) VALUES (?, ?)', (url, score))
        count += 1
    conn.commit()
    conn.close()
    print(f"Saved {count} pagerank scores")

def load_index():
    conn = sqlite3.connect('search_engine.db')
    c = conn.cursor()
    
    # Load inverted index
    c.execute('SELECT word, url FROM index_table')
    index = {}
    for word, url in c.fetchall():
        if word not in index:
            index[word] = []
        index[word].append(url)
    
    # Load TF scores
    c.execute('SELECT url, word, tf_score FROM tfidf')
    tf_scores = {}
    for url, word, score in c.fetchall():
        if url not in tf_scores:
            tf_scores[url] = {}
        tf_scores[url][word] = score
    
    # Load IDF scores
    c.execute('SELECT word, idf_score FROM idf_table')
    idf_scores = {word: score for word, score in c.fetchall()}
    
    conn.close()
    return index, tf_scores, idf_scores

def load_pagerank():
    conn = sqlite3.connect('search_engine.db')
    c = conn.cursor()
    c.execute('SELECT url, pagerank FROM pages')
    ranks = {url: score for url, score in c.fetchall() if score is not None}
    conn.close()
    return ranks

def load_page_content():
    conn = sqlite3.connect('search_engine.db')
    c = conn.cursor()
    c.execute('SELECT url, content FROM pages')
    content = {url: text for url, text in c.fetchall()}
    conn.close()
    return content