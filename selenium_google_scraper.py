import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sys

def google_scholar_search_selenium(query):
    # Setup Chrome options
    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
    options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration (sometimes required in headless mode)
    options.add_argument('--no-sandbox')  # Avoids issues when running on a server or Docker environment
    options.add_argument('--window-size=1920x1080')  # Set the window size for headless mode (can help prevent rendering issues)

    # Initialize the WebDriver with Chrome options
    driver = webdriver.Chrome(options=options)

    base_url = "https://scholar.google.com/scholar"
    search_results = []

    # Loop through the pages of Google Scholar results (10 results per page)
    for page in range(0, 30, 10):  # Loop through 3 pages (30 results)
        params = {"q": query, "start": page}
        driver.get(f"{base_url}?q={query}&start={page}")

        # Wait for the page to load
        time.sleep(random.uniform(3, 5))  # Random sleep to mimic human behavior

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', class_='gs_r')

        for result in results:
            title_tag = result.find('h3')
            link_tag = result.find('a', href=True)
            if title_tag and link_tag:
                title = title_tag.text.strip()
                link = link_tag['href']
                result_str = f"{title}\n{link}\n"
                search_results.append(result_str)

                # Print results to the console in real-time
                print(result_str)

        # Add a delay to avoid detection
        time.sleep(random.uniform(3, 5))  # Sleep between 3 and 5 seconds

    # Close the WebDriver
    driver.quit()

    return search_results

# Main function to handle command-line arguments and call the search function
if __name__ == "__main__":
    # Get the query from the command-line argument
    if len(sys.argv) < 2:
        print("Usage: python selenium_google_scraper.py <search_query>")
        sys.exit(1)

    query = sys.argv[1]  # The search query passed from the Bash script

    # Call the function to scrape Google Scholar
    results = google_scholar_search_selenium(query)

    # Optionally, you can print the total results after scraping all pages.
    if not results:
        print("No results found.")
