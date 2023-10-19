import requests
from flask import Flask, jsonify, request

app = Flask(__name)

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

def get_recent_news():
    params = {
        "action": "query",
        "format": "json",
        "list": "recentchanges",
        "rcnamespace": "0",
        "rclimit": 10,
        "rcshow": "!minor|!bot",
        "rctype": "edit|new",
    }

    response = requests.get(WIKIPEDIA_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("query", {}).get("recentchanges", [])
    else:
        return []

@app.route('/news', methods=['GET'])
def get_news():
    news_articles = get_recent_news()
    if news_articles:
        return jsonify({"news": news_articles})
    else:
        return jsonify({"error": "Failed to fetch news articles from Wikipedia"})

if __name__ == '__main__':
    app.run(debug=True)
    # http://localhost:5000/news
