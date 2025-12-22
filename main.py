import pandas as pd
import os
from scrapers.brighter_monday import BrighterMondayScraper
from database.db import JobDatabase
from utils.logger import logger
from utils.cleaner import clean_job_data


def run():
    logger.info("🚀 Starting Job Aggregator...")

    # Initialize Scraper and DB
    scraper = BrighterMondayScraper()
    db = JobDatabase()

    # 1. Scrape
    jobs = scraper.scrape()

    if jobs:
        # 2. Save to Database (Handles duplicates automatically via unique link)
        db.save_jobs(jobs)

        # 3. Process and Clean for CSV
        df = pd.DataFrame(jobs)
        df = clean_job_data(df)

        # Ensure output folder exists
        output_path = "output/jobs.csv"
        if not os.path.exists('output'):
            os.makedirs('output')

        try:
            # 4. Export to CSV
            df.to_csv(output_path, index=False)
            logger.info(f"💾 Saved {len(df)} jobs to {output_path}")

            # 5. Automatically open in Excel (Windows default for .csv)
            logger.info("📊 Opening results in Excel...")
            os.startfile(os.path.abspath(output_path))

        except PermissionError:
            logger.error(f"❌ Could not update {output_path}. Please CLOSE the file in Excel first!")

        logger.info("✨ Process complete!")
    else:
        logger.error("❌ No jobs found. Check your internet connection or website selectors.")


if __name__ == "__main__":
    run()