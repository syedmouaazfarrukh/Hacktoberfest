import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name)

def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def extract_festivals(search_html):
    soup = BeautifulSoup(search_html, 'html.parser')
    results = []

    for div in soup.find_all("div", {"class": "tF2Cxc"}):
        title = div.find("h3").text
        results.append(title)

    return results

@app.route('/get_festivals', methods=['GET'])
def get_festivals():
    year = request.args.get('year', type=int)
    query = f"{year} festivals"
    search_html = google_search(query)

    if search_html:
        festivals = extract_festivals(search_html)
        if festivals:
            return jsonify({"Year": year, "Festivals": festivals})
        else:
            return jsonify({"error": "No festivals found in the search results."})
    else:
        return jsonify({"error": "Failed to retrieve search results."})

if __name__ == '__main__':
    app.run(debug=True)
# http://localhost:5000/get_festivals?year=your_year
