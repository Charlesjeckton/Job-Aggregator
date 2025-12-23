import pandas as pd
import os
import datetime
import glob
from scrapers import (
    BrighterMondayScraper,
    MyJobMagScraper,
    FuzuScraper,
    ReliefWebScraper,
    JobWebKenyaScraper,
    UNCareersScraper,
    UNDPScraper,
    UNICEFScraper,
    IndeedScraper,
    KenyaJobsComScraper
)
from database.db import JobDatabase
from utils.logger import logger
from utils.cleaner import clean_job_data


def cleanup_old_reports(folder='output', keep=5):
    """Deletes old CSV reports to keep the workspace clean."""
    files = sorted(glob.glob(os.path.join(folder, "jobs_report_*.csv")))
    if len(files) > keep:
        for f in files[:-keep]:
            try:
                os.remove(f)
            except Exception as e:
                logger.error(f"Failed to delete old file {f}: {e}")


def run():
    logger.info("🚀 Starting Multi-Site Job Aggregator...")

    # 1. Initialize Folders & Database
    for folder in ['output', 'logs']:
        if not os.path.exists(folder):
            os.makedirs(folder)

    cleanup_old_reports()  # Keep only the 5 most recent files
    db = JobDatabase()

    # 2. Define all active scraper instances
    active_scrapers = [
        BrighterMondayScraper(),
        MyJobMagScraper(),
        FuzuScraper(),
        ReliefWebScraper(),
        UNICEFScraper(),
        UNDPScraper(),
        IndeedScraper(),
        KenyaJobsComScraper(),
        UNCareersScraper(),
        JobWebKenyaScraper()
    ]

    all_jobs = []

    # 3. Loop through each scraper
    for scraper in active_scrapers:
        scraper_name = scraper.__class__.__name__
        logger.info(f"🔍 Scraping {scraper_name}...")

        try:
            site_jobs = scraper.scrape()
            if site_jobs:
                logger.info(f"✅ {scraper_name} found {len(site_jobs)} jobs.")
                all_jobs.extend(site_jobs)
                # Save to Database (Duplicates handled by unique 'link' constraint)
                db.save_jobs(site_jobs)
            else:
                logger.warning(f"⚠️ No jobs found for {scraper_name}.")
        except Exception as e:
            logger.error(f"❌ Error during {scraper_name} run: {e}")

    # 4. Process and Export Results
    if all_jobs:
        df = pd.DataFrame(all_jobs)
        df = clean_job_data(df)

        # 5. Smart Console Highlighter
        if 'relevance_score' in df.columns:
            df = df.sort_values(by="relevance_score", ascending=False)

            # Show top 5 "Gold" matches in the terminal
            high_relevance = df[df['relevance_score'] >= 90]
            if not high_relevance.empty:
                logger.info(f"🔥 Found {len(high_relevance)} HIGH-RELEVANCE jobs (Intern/Junior)!")
                for i, row in high_relevance.head(5).iterrows():
                    # Safely handle 'company' if column exists
                    company_str = f" at {row['company']}" if 'company' in row and pd.notna(row['company']) else ""
                    logger.info(f"   ⭐ {row['title']}{company_str}")

        # Unique filename using the current time
        timestamp = datetime.datetime.now().strftime("%H%M")
        output_path = os.path.abspath(f"output/jobs_report_{timestamp}.csv")

        try:
            df.to_csv(output_path, index=False)
            logger.info(f"💾 Total collection saved: {len(df)} jobs to {output_path}")

            # 6. Open in Excel
            logger.info(f"📊 Opening {os.path.basename(output_path)} in Excel...")
            os.startfile(output_path)

        except Exception as e:
            logger.error(f"❌ Failed to save or open CSV: {e}")

        logger.info("✨ Full Aggregation Process Complete!")
    else:
        logger.error("❌ No jobs found across all platforms.")


if __name__ == "__main__":
    run()
