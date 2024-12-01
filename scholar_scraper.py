import sys
import requests
import time
import random
from bs4 import BeautifulSoup

def google_scholar_search(query):
    base_url = "https://scholar.google.com/scholar"
    search_results = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for page in range(0, 30, 10):
        params = {"q": query, "start": page}
        
        try:
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses

            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='gs_r')

            for result in results:
                title_tag = result.find('h3')
                link_tag = result.find('a', href=True)
                if title_tag and link_tag:
                    title = title_tag.text.strip()
                    link = link_tag['href']
                    search_results.append(f"{title}\n{link}\n")

            # Add delay to prevent rate limiting
            time.sleep(random.uniform(1, 3))  # Sleep between 1 and 3 seconds

        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to retrieve page {page // 10 + 1}: {e}")
            time.sleep(5)  # Wait before retrying the same page
            continue

    return search_results

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scholar_scraper.py <search_query>")
        sys.exit(1)

    query = sys.argv[1]
    results = google_scholar_search(query)

    if results:
        for result in results:
            print(result)
    else:
        print("No results found.")

if __name__ == "__main__":
    main()

