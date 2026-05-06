from flask import Flask, request, render_template_string
from search import search
from indexer import load_index
from pagerank import load_pagerank

app = Flask(__name__)

print("Loading data...")
index = load_index()
ranks = load_pagerank()

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
        .result { margin: 20px 0; }
        .result a { color: #1a0dab; font-size: 18px; text-decoration: none; }
        .result a:hover { text-decoration: underline; }
        .score { color: #666; font-size: 12px; }
        .url { color: #006621; font-size: 14px; }
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
        {% for url, score in results %}
        <div class="result">
            <div class="url">{{ url }}</div>
            <a href="{{ url }}" target="_blank">{{ url.split('/wiki/')[-1].replace('_', ' ') }}</a>
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
    results = search(query, index, ranks) if query else []
    return render_template_string(HTML, query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)