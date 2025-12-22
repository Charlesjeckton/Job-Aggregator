import requests
from bs4 import BeautifulSoup
from utils.cleaner import clean_text  # Import your updated cleaner

class BaseScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_page(self, url):
        """Fetches the page content and returns a BeautifulSoup object."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return BeautifulSoup(response.text, 'html.parser')
            print(f"Failed to fetch {url}: Status {response.status_code}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    def get_clean_text(self, element):
        """
        Helper to extract text from a BS4 element and clean it automatically.
        Pass a soup element like soup.find('p') here.
        """
        if element:
            return clean_text(element.get_text())
        return "N/A"
