# scrapers/unicef_scraper.py
from urllib.parse import urljoin
import time
import random
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from utils.logger import logger

# Optional fallback
import cloudscraper

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

class UNICEFScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://jobs.unicef.org/en-us/search/?search-keyword=")
        self.logger = logger
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )

    def scrape(self):
        all_jobs = []

        # --- Playwright Scraper (Primary) ---
        try:
            self.logger.info("📡 Scraping UNICEF Global Vacancies (Playwright)...")
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(self.base_url, timeout=60000)
                time.sleep(random.uniform(3, 6))  # Allow JS to populate listings

                # Wait for job items to appear
                try:
                    page.wait_for_selector("tr.job-external, a.job-link, div.job-listing", timeout=15000)
                except PlaywrightTimeout:
                    self.logger.warning("⚠️ No job rows found in UNICEF page DOM.")

                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')

                job_items = soup.find_all('tr', class_='job-external') or \
                            soup.select('a.job-link') or \
                            soup.select('div.job-listing')

                for item in job_items:
                    try:
                        link_el = item if item.name == 'a' else item.find('a', class_='job-link')
                        if not link_el:
                            continue
                        title = link_el.get_text(strip=True)
                        link = urljoin(self.base_url, link_el['href'])

                        parent = item.find_parent('tr') if item.name != 'tr' else item
                        cells = parent.find_all('td') if parent else []

                        location = cells[1].get_text(strip=True) if len(cells) > 1 else "Global"
                        deadline = cells[2].get_text(strip=True) if len(cells) > 2 else "Check Link"

                        score = 85
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

                browser.close()

            if all_jobs:
                return all_jobs
        except Exception as e:
            self.logger.warning(f"⚠️ Playwright scraping failed: {e}")

        # --- Cloudscraper Fallback ---
        try:
            self.logger.info("📡 Trying Cloudscraper fallback for UNICEF...")
            time.sleep(random.uniform(3, 5))
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36',
                'Referer': 'https://jobs.unicef.org/'
            }
            response = self.scraper.get(self.base_url, headers=headers, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            job_items = soup.find_all('tr', class_='job-external') or soup.select('a.job-link')

            for item in job_items:
                try:
                    link_el = item if item.name == 'a' else item.find('a', class_='job-link')
                    if not link_el: continue

                    title = link_el.get_text(strip=True)
                    link = urljoin(self.base_url, link_el['href'])

                    parent = item.find_parent('tr') if item.name != 'tr' else item
                    cells = parent.find_all('td') if parent else []

                    location = cells[1].get_text(strip=True) if len(cells) > 1 else "Global"
                    deadline = cells[2].get_text(strip=True) if len(cells) > 2 else "Check Link"

                    score = 85
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
            self.logger.error(f"❌ UNICEF fallback failed: {e}")
            return []
