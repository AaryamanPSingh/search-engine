from flask import Flask, request, render_template_string
from search import search, get_snippet
from indexer import load_index
from pagerank import load_pagerank
from crawler import load_data

app = Flask(__name__)

print("Loading data...")
index, tf_scores, idf_scores = load_index()
ranks = load_pagerank()
_, page_content = load_data()

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>MathSearch</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 0 20px; }
        h1 { color: #4285f4; }
        input[type="text"] { width: 70%; padding: 10px; font-size: 16px; border: 1px solid #ddd; border-radius: 4px; }
        button { padding: 10px 20px; background: #4285f4; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        .result { margin: 25px 0; }
        .result a { color: #1a0dab; font-size: 18px; text-decoration: none; }
        .result a:hover { text-decoration: underline; }
        .score { color: #666; font-size: 12px; }
        .url { color: #006621; font-size: 14px; }
        .snippet { color: #333; font-size: 14px; margin-top: 4px; }
    </style>
</head>
<body>
    <h1>🔢 MathSearch</h1>
    <form method="GET" action="/search">
        <input type="text" name="q" value="{{ query }}" placeholder="Search mathematics...">
        <button type="submit">Search</button>
    </form>
    {% if results %}
        <p>Top results for <b>{{ query }}</b>:</p>
        {% for url, score, snippet in results %}
        <div class="result">
            <div class="url">{{ url }}</div>
            <a href="{{ url }}" target="_blank">{{ url.split('/wiki/')[-1].replace('_', ' ') }}</a>
            <div class="snippet">{{ snippet }}</div>
            <div class="score">PageRank: {{ "%.10f"|format(score) }}</div>
        </div>
        {% endfor %}
    {% endif %}
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML, query='', results=[])

@app.route('/search')
def search_page():
    query = request.args.get('q', '')
    if query:
        raw_results = search(query, index, tf_scores, idf_scores, ranks)
        results = [(url, score, get_snippet(url, query, page_content)) 
                   for url, score in raw_results]
    else:
        results = []
    return render_template_string(HTML, query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)