from .base_scraper import BaseScraper
from urllib.parse import urljoin


class ReliefWebScraper(BaseScraper):
    def __init__(self):
        # Filtered specifically for Kenya
        super().__init__("https://reliefweb.int/jobs?list=Kenya%20Jobs")

    def scrape(self):
        soup = self.fetch_page(self.base_url)
        if not soup: return []

        jobs_list = []
        # ReliefWeb uses 'article' tags for job cards
        items = soup.find_all('article', class_='rw-river-article--job')

        for item in items:
            try:
                title_link = item.find('h3', class_='rw-river-article__title').find('a')
                title = self.get_clean_text(title_link)
                link = urljoin(self.base_url, title_link['href'])

                # Score roles related to Tech or Internships
                score = 0
                if any(kw in title.lower() for kw in ["data", "ict", "software", "information"]):
                    score += 50
                if "intern" in title.lower():
                    score += 40

                jobs_list.append({
                    "title": title,
                    "link": link,
                    "relevance_score": score
                })
            except Exception:
                continue

        return jobs_list
