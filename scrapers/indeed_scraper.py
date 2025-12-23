# scrapers/indeed_scraper.py
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
from .base_scraper import BaseScraper
from utils.logger import logger


class IndeedScraper(BaseScraper):
    def __init__(self):
        # We use a broader query to ensure results
        super().__init__("https://ke.indeed.com/jobs?q=intern&l=Nairobi&fromage=3")
        self.logger = logger
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )

    def scrape(self):
        all_jobs = []
        try:
            self.logger.info("📡 Scraping Indeed (Bypassing DNS/Cloudflare)...")
            time.sleep(random.uniform(8, 12))

            # Critical headers for Indeed 2025
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.google.com/'
            }

            response = self.scraper.get(self.base_url, headers=headers, timeout=20)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Updated 2025 Selectors
            job_cards = soup.select('.job_seen_beacon') or soup.select('td.resultContent')

            for card in job_cards:
                title_el = card.select_one('a[id^="job_"]') or card.select_one('.jcs-JobTitle')
                if not title_el: continue

                title = title_el.get_text(strip=True)
                link = urljoin("https://ke.indeed.com", title_el['href'])
                company = card.select_one('[data-testid="company-name"]')

                all_jobs.append({
                    "title": title,
                    "company": company.text if company else "Indeed Employer",
                    "link": link,
                    "relevance_score": 95 if "intern" in title.lower() else 80
                })
            return all_jobs
        except Exception as e:
            self.logger.error(f"❌ Indeed Failed (Check Internet/DNS): {e}")
            return []