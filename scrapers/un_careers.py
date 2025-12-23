import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
from .base_scraper import BaseScraper
from utils.logger import logger


class UNCareersScraper(BaseScraper):
    def __init__(self):
        # Specific search string that forces English and lists recent jobs
        super().__init__("https://careers.un.org/jobopening?language=en")

    def scrape(self):
        all_jobs = []
        try:
            self.logger.info("📡 Scanning UN Internship Portal (Direct Query)...")
            time.sleep(random.uniform(5, 8))  # Give extra time for the grid to load

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Referer': 'https://careers.un.org/home'
            }

            response = self.scraper.get(self.base_url, headers=headers, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 2025 UN Selectors: The UN uses a specific "row-link" or
            # divs containing "Job ID" and "Duty Station"
            job_items = soup.find_all('tr', class_='row-link') or \
                        soup.select('div.job-opening-item') or \
                        soup.find_all('tr', id=lambda x: x and 'dgJobResults' in x)

            if not job_items:
                # Emergency fallback: look for anything containing 'View Job Description'
                job_items = [link.find_parent('tr') for link in soup.find_all('a') if
                             'View Job Description' in link.text]

            for item in job_items:
                try:
                    link_el = item.find('a', href=True)
                    if not link_el: continue

                    link = urljoin(self.base_url, link_el['href'])
                    full_text = item.get_text(separator=' ', strip=True)

                    # UN Titles often look like "INTERN - Information Management"
                    title = link_el.get_text(strip=True)
                    if not title or "View Job" in title:
                        # Try to find the title in the first sibling <td>
                        title = item.find_all('td')[0].text.strip()

                    # Specific Nairobi/Tech relevance
                    score = 80
                    if "NAIROBI" in full_text.upper():
                        score += 15
                    if any(kw in title.lower() for kw in ["ict", "tech", "data", "software"]):
                        score = 100

                    all_jobs.append({
                        "title": title,
                        "company": "United Nations",
                        "link": link,
                        "relevance_score": score
                    })
                except Exception:
                    continue

            return all_jobs

        except Exception as e:
            self.logger.error(f"❌ UN Careers Error: {e}")
            return []