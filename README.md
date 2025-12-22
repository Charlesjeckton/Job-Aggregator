# 🚀 AI-Powered Job Aggregator

A robust Python-based web scraping tool designed to automatically find, clean, and store internship and junior-level job listings. This project focuses on **BrighterMonday Kenya**, helping entry-level professionals automate their job search.

## ✨ Features
* **Automated Scraping:** Extracts job titles and direct links from BrighterMonday.
* **Intelligent Scoring:** Automatically calculates a `relevance_score` based on keywords (e.g., Intern, Junior, Graduate).
* **Data Persistence:** Saves unique job listings to an **SQLite Database** to prevent duplicates and exports a clean **CSV** for daily viewing.
* **Excel Integration:** Automatically opens the results in Excel upon completion.
* **Robust Logging:** Detailed timestamped logs for tracking successes and errors.
* **Bot-Detection Bypass:** Implements human-like delays and browser-mimicking headers.

## 📂 Project Structure
```text
job_aggregator/
│
├── scrapers/          # Scraper logic and base classes
├── database/          # SQLite DB storage and management
├── utils/             # Data cleaning and logging utilities
├── output/            # Generated CSV reports
├── logs/              # History of scraper runs
├── main.py            # Entry point for the application
├── run_aggregator.bat # One-click Windows runner
└── requirements.txt   # Required Python libraries