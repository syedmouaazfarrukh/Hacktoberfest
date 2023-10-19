from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def extract_first_result(search_html):
    soup = BeautifulSoup(search_html, 'html.parser')
    result_div = soup.find("div", {"class": "tF2Cxc"})
    if result_div:
        title = result_div.find("h3").text
        link = result_div.find("a")["href"]
        return title, link
    else:
        return None, None

@app.get("/get_first_result/")
async def get_first_result(query: str):
    search_html = google_search(query)

    if search_html:
        title, link = extract_first_result(search_html)
        if title and link:
            return {"Title": title, "URL": link}
        else:
            return {"error": "No search results found."}
    else:
        return {"error": "Failed to retrieve search results."}

# http://localhost:8000/get_first_result/?query=your_query
