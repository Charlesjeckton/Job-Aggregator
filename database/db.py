import sqlite3
from utils.logger import logger


class JobDatabase:
    def __init__(self, db_name="database/jobs.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        """Creates the jobs table if it doesn't exist."""
        query = """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            link TEXT UNIQUE,
            relevance_score INTEGER,
            date_scraped DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            self.conn.execute(query)
            self.conn.commit()
        except Exception as e:
            logger.error(f"Database error: {e}")

    def save_jobs(self, jobs_list):
        """Saves a list of job dictionaries to the database."""
        added_count = 0
        for job in jobs_list:
            try:
                query = "INSERT INTO jobs (title, company, location, link, relevance_score) VALUES (?, ?, ?, ?, ?)"
                self.conn.execute(query, (
                    job.get('title'),
                    job.get('company', 'N/A'),
                    job.get('location', 'Kenya'),
                    job.get('link'),
                    job.get('relevance_score', 0)
                ))
                added_count += 1
            except sqlite3.IntegrityError:
                # This happens if the link already exists in the DB
                continue

        self.conn.commit()
        logger.info(f"🗄️ Database: {added_count} new jobs saved.")