import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
from .base_scraper import BaseScraper
from utils.logger import logger


class UNICEFScraper(BaseScraper):
    def __init__(self):
        # Targeting the main search/vacancies page
        super().__init__("https://jobs.unicef.org/en-us/search/?search-keyword=")
        self.logger = logger
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )

    def scrape(self):
        all_jobs = []
        try:
            self.logger.info("📡 Scraping UNICEF Global Vacancies...")
            # UNICEF needs a slightly longer "human-like" pause
            time.sleep(random.uniform(5, 8))

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Referer': 'https://jobs.unicef.org/'
            }

            response = self.scraper.get(self.base_url, headers=headers, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 2025 Selectors: UNICEF uses a table with class 'job-external'
            # or items with class 'job-link'
            job_items = soup.find_all('tr', class_='job-external') or \
                        soup.select('.job-link') or \
                        soup.find_all('a', class_='job-link')

            for item in job_items:
                try:
                    # If item is the <a> itself, use it; otherwise find the <a> inside
                    link_el = item if item.name == 'a' else item.find('a', class_='job-link')
                    if not link_el: continue

                    title = link_el.get_text(strip=True)
                    link = urljoin(self.base_url, link_el['href'])

                    # Metadata (Location/Closing date) is often in siblings or parent rows
                    parent = item.find_parent('tr') if item.name != 'tr' else item
                    cells = parent.find_all('td') if parent else []

                    location = cells[1].get_text(strip=True) if len(cells) > 1 else "Global"
                    deadline = cells[2].get_text(strip=True) if len(cells) > 2 else "Check Link"

                    # Relevance Scoring
                    score = 85
                    # Boost for local roles or high-demand tech roles
                    if "NAIROBI" in location.upper() or "KENYA" in location.upper():
                        score += 10
                    if any(kw in title.lower() for kw in ["ict", "data", "software", "innovation", "technology"]):
                        score = 100

                    all_jobs.append({
                        "title": f"{title} (Deadline: {deadline})",
                        "company": f"UNICEF - {location}",
                        "link": link,
                        "relevance_score": score
                    })
                except Exception:
                    continue

            return all_jobs

        except Exception as e:
            self.logger.error(f"❌ UNICEF Scraper Error: {e}")
            return []