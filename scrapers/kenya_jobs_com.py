import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
from .base_scraper import BaseScraper
from utils.logger import logger


class KenyaJobsComScraper(BaseScraper):
    def __init__(self):
        # Targeting the main search results page
        super().__init__("https://www.kenyajob.com/job-vacancies-search-kenya")
        self.logger = logger
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )

    def scrape(self):
        all_jobs = []
        try:
            self.logger.info("📡 Scraping KenyaJobs.com...")
            # Respectful delay even though bot protection is low
            time.sleep(random.uniform(3, 5))

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Referer': 'https://www.kenyajob.com/'
            }

            response = self.scraper.get(self.base_url, headers=headers, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 2025 Selectors: Jobs are often listed in rows with class 'job-description-wrapper'
            # or simple search-result containers.
            job_containers = soup.select('.job-description-wrapper') or \
                             soup.select('.search-results .job-item') or \
                             soup.find_all('div', class_='col-lg-12 col-md-12 col-sm-12 col-xs-12')

            for item in job_containers:
                try:
                    # Look for the title link
                    link_el = item.find('a', href=True)
                    if not link_el or 'job-vacancies' not in link_el['href']:
                        continue

                    title = link_el.get_text(strip=True)
                    link = urljoin(self.base_url, link_el['href'])

                    # Company info is usually in a sub-element or sibling
                    company_el = item.find('div', class_='company-name') or item.find('p')
                    company = company_el.get_text(strip=True) if company_el else "KenyaJobs Employer"

                    # Relevance Scoring for Tech/Internships
                    score = 85
                    if any(kw in title.lower() for kw in ["intern", "attachment", "trainee"]):
                        score += 5
                    if any(kw in title.lower() for kw in ["ict", "it ", "software", "data", "developer"]):
                        score = 100

                    all_jobs.append({
                        "title": title,
                        "company": company,
                        "link": link,
                        "relevance_score": score
                    })
                except Exception:
                    continue

            return all_jobs

        except Exception as e:
            self.logger.error(f"❌ KenyaJobs.com Error: {e}")
            return []