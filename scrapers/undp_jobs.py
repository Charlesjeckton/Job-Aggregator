import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
from .base_scraper import BaseScraper
from utils.logger import logger


class UNDPScraper(BaseScraper):
    def __init__(self):
        # Targeting the 'All Vacancies' page with a forced language parameter
        self.target_url = "https://jobs.undp.org/cj_view_jobs.cfm?cur_lang=en"
        super().__init__(self.target_url)
        self.logger = logger
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )

    def scrape(self):
        all_jobs = []
        try:
            self.logger.info("📡 Scanning UNDP Global Vacancy Grid...")
            # UNDP requires a human-like delay to bypass the initial load shield
            time.sleep(random.uniform(5, 8))

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Referer': 'https://www.undp.org/careers',
            }

            response = self.scraper.get(self.target_url, headers=headers, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 2025 UNDP Selector: The jobs are inside a table with ID "dgJobResults"
            # We target all rows (tr) within that table
            job_rows = soup.select('table#dgJobResults tr') or soup.find_all('tr')

            for row in job_rows:
                try:
                    # Look for the title link which points to cj_view_job.cfm
                    link_el = row.find('a', href=lambda x: x and 'cj_view_job.cfm' in x)
                    if not link_el:
                        continue

                    title = link_el.get_text(strip=True)
                    link = urljoin(self.target_url, link_el['href'])

                    # Columns: 0=Title, 1=Post Level, 2=Agency, 3=Location
                    cells = row.find_all('td')
                    post_level = cells[1].get_text(strip=True) if len(cells) > 1 else "N/A"
                    agency = cells[2].get_text(strip=True) if len(cells) > 2 else "UNDP"
                    location = cells[3].get_text(strip=True) if len(cells) > 3 else "Global"

                    # Scoring logic: High priority for Nairobi, Tech, and Internships
                    score = 80
                    if "NAIROBI" in location.upper() or "KENYA" in location.upper():
                        score += 15
                    if any(kw in title.lower() for kw in ["ict", "tech", "data", "software"]):
                        score = 100
                    if "intern" in post_level.lower() or "intern" in title.lower():
                        score = 100

                    all_jobs.append({
                        "title": f"{title} [{post_level}]",
                        "company": f"{agency} - {location}",
                        "link": link,
                        "relevance_score": score
                    })
                except Exception:
                    continue

            if not all_jobs:
                self.logger.warning("⚠️ Selector check: Found 0 jobs. The site structure may have updated.")
            else:
                self.logger.info(f"✅ UNDPScraper successfully found {len(all_jobs)} jobs.")

            return all_jobs

        except Exception as e:
            self.logger.error(f"❌ UNDP Scraper critical failure: {e}")
            return []