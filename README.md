# 📌 Internship Job Scraper (Kenya)

## 📖 Overview
This project is a Python-based job scraper that collects internship opportunities from multiple Kenyan job platforms. It automates the process of searching, filtering, and exporting job listings into a structured Excel file for easy tracking and application.

The scraper focuses on entry-level tech roles such as:
- Junior Developer
- IT Support
- Software Engineering Internships
- Other IT-related roles

---

## 🚀 Features
- 🔍 Scrapes multiple job platforms:
  - BrighterMonday  
  - MyJobMag  
  - Fuzu   
  - KenyanJobsConnection  

- 🎯 Keyword-based filtering (e.g., *Internship*, *Junior Developer*, *IT Support*)
- 📅 Extracts key job details:
  - Job Title  
  - Company Name  
  - Location  
  - Posting Date  
  - Job Link  

- 📊 Exports results to Excel
- ⚡ Modular structure for easy extension

---

## 🛠️ Tech Stack
- Python 3.x  
- requests  
- BeautifulSoup  
- pandas  
- openpyxl


internship-scraper/
│
├── scrapers/
│   ├── brightermonday.py
│   ├── myjobmag.py
│   ├── fuzu.py
│   ├── linkedin.py
│   └── kenyanjobs.py
│
├── utils/
│   └── helpers.py
│
├── output/
│   └── internships.xlsx
│
├── main.py
├── requirements.txt
└── README.md

---

## 📂 Project Structure
