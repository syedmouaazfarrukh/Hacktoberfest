import requests
from bs4 import BeautifulSoup

def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to retrieve search results.")
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

if __name__ == "__main__":
    query = input("Enter your Google search query: ")
    search_html = google_search(query)

    if search_html:
        title, link = extract_first_result(search_html)
        if title and link:
            print("First search result:")
            print("Title:", title)
            print("URL:", link)
        else:
            print("No search results found.")
