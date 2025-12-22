import time
import random
from urllib.parse import urljoin
from .base_scraper import BaseScraper

class BrighterMondayScraper(BaseScraper):
    def __init__(self):
        # We target the main jobs page
        super().__init__("https://www.brightermonday.co.ke/jobs")

    def scrape(self):
        # 1. Improved headers to bypass basic bot detection
        self.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
        })

        # 2. Fetch the page
        soup = self.fetch_page(self.base_url)
        jobs_list = []

        if not soup:
            return []

        # 3. Enhanced Selectors: BrighterMonday often wraps cards in these classes
        # We use a list of possible selectors to be robust
        items = soup.select('div.flex.flex-1.flex-col') or \
                soup.select('div[class*="flex-grow"]') or \
                soup.find_all('div', class_='mx-3')

        for item in items:
            # Look for titles in standard job link classes or common paragraph tags
            title_el = item.find('p', class_='text-lg') or \
                       item.find('a', class_='metrics-site-gather-job-click') or \
                       item.find('p', class_='font-semibold')

            if title_el:
                title = self.get_clean_text(title_el)

                # Find the link
                link_el = item.find('a') if item.name != 'a' else item
                link = urljoin(self.base_url, link_el['href']) if link_el and link_el.has_attr('href') else "N/A"

                if title == "N/A" or not title: 
                    continue

                # 4. Scoring Logic
                score = 0
                title_lower = title.lower()
                if "intern" in title_lower: score += 50
                if "junior" in title_lower: score += 30
                if "graduate" in title_lower: score += 20

                jobs_list.append({
                    "title": title,
                    "link": link,
                    "relevance_score": score
                })

        # Human-like delay
        time.sleep(random.uniform(1, 3))
        return jobs_list