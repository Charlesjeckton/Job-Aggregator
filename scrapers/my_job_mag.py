from urllib.parse import urljoin
from .base_scraper import BaseScraper


class MyJobMagScraper(BaseScraper):
    def __init__(self):
        # Targeting the latest jobs in Kenya
        super().__init__("https://www.myjobmag.co.ke/jobs-by-field/information-technology")

    def scrape(self):
        soup = self.fetch_page(self.base_url)
        jobs_list = []

        if not soup:
            return []

        # MyJobMag wraps jobs in <li> tags with class 'job-info'
        items = soup.find_all('li', class_='job-info')

        for item in items:
            # Title and Link are usually inside an <h2> or <a> tag
            title_el = item.find('h2') or item.find('a')
            if title_el:
                title = self.get_clean_text(title_el)

                # Link handling
                link_el = title_el.find('a') if title_el.name != 'a' else title_el
                raw_link = link_el['href'] if link_el and link_el.has_attr('href') else ""
                full_link = urljoin(self.base_url, raw_link)

                # Metadata: Company and Location
                # MyJobMag usually lists these in sub-lists or spans
                score = 0
                title_lower = title.lower()
                if any(word in title_lower for word in ["intern", "graduate", "junior", "entry"]):
                    score = 80

                jobs_list.append({
                    "title": title,
                    "link": full_link,
                    "relevance_score": score
                })

        return jobs_list
