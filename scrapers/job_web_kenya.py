from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
import time
import random
from .base_scraper import BaseScraper
from utils.logger import logger

class JobWebKenyaScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://jobwebkenya.com/job-type/internship/")
        self.logger = logger
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape(self):
        all_jobs = []
        for page_num in range(1, 4):
            page_url = self.base_url if page_num == 1 else urljoin(self.base_url, f"page/{page_num}/")
            try:
                self.logger.info(f"📡 Scraping JobWebKenya: Page {page_num}...")
                self.driver.get(page_url)
                time.sleep(random.uniform(4, 6))  # Wait for JS to load

                items = self.driver.find_elements(By.CSS_SELECTOR, "li.job_listing, .job-list-content, article")
                self.logger.info(f"Found {len(items)} job elements on page {page_num}")

                if not items:
                    continue

                for item in items:
                    try:
                        link_el = item.find_element(By.TAG_NAME, "a")
                        full_text = link_el.text.strip()
                        link = urljoin(self.base_url, link_el.get_attribute("href"))

                        title, company = full_text, "N/A"
                        if " at " in full_text:
                            parts = full_text.split(" at ")
                            title, company = parts[0].strip(), parts[1].strip()

                        score = 100 if any(kw in title.lower() for kw in ["ict", "it ", "software", "data", "tech", "computer"]) else 90

                        all_jobs.append({
                            "title": title,
                            "company": company,
                            "link": link,
                            "relevance_score": score
                        })
                    except Exception:
                        continue

            except Exception as e:
                self.logger.error(f"❌ Error on Page {page_num}: {e}")
                continue

        self.driver.quit()
        return all_jobs
