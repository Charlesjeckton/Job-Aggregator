import time
import random
import cloudscraper
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper


class FuzuScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.fuzu.com/kenya/job")
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )

    def scrape(self):
        try:
            # Human-like delay is crucial for Fuzu
            time.sleep(random.uniform(5, 8))

            response = self.scraper.get(self.base_url, timeout=20)
            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            jobs_list = []

            # 2025 FUZU SELECTOR STRATEGY:
            # Look for any anchor tag that contains '/job/' in the URL.
            # This is more reliable than specific class names which change often.
            items = soup.find_all('a', href=lambda x: x and '/kenya/job/' in x)

            for item in items:
                try:
                    # Title is usually the strongest text inside the card
                    # We check h2, h3, or just the main text of the link
                    title_el = item.find(['h2', 'h3', 'p'])
                    title = self.get_clean_text(title_el) if title_el else item.get_text(strip=True)

                    if len(title) < 5 or "apply" in title.lower():
                        continue

                    link = urljoin(self.base_url, item['href'])

                    # Scoring logic for Junior/Intern roles
                    score = 0
                    t_lower = title.lower()
                    if any(kw in t_lower for kw in ["intern", "graduate", "junior", "trainee"]):
                        score = 90
                    elif any(kw in t_lower for kw in ["python", "data", "software", "dev"]):
                        score += 20

                    jobs_list.append({
                        "title": title,
                        "link": link,
                        "relevance_score": score
                    })
                except Exception:
                    continue

            # Remove duplicates that might occur due to multiple links in one card
            unique_jobs = {job['link']: job for job in jobs_list}.values()
            return list(unique_jobs)

        except Exception as e:
            print(f"Fuzu Scraper Error: {e}")
            return []
