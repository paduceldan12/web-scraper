import requests
from bs4 import BeautifulSoup
import csv

# Define the target URL (example: scraping job listings from 'remoteok.io')
URL = "https://remoteok.io/remote-dev-jobs"

# Headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

def fetch_jobs():
    """Scrape job listings from RemoteOK"""
    response = requests.get(URL, headers=HEADERS)
    
    if response.status_code != 200:
        print("Failed to retrieve data")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    # Finding all job listing rows
    job_rows = soup.find_all("tr", class_="job")

    for job in job_rows:
        title_tag = job.find("h2", itemprop="title")
        company_tag = job.find("h3", itemprop="name")
        link_tag = job.find("a", class_="preventLink")

        if title_tag and company_tag and link_tag:
            job_title = title_tag.text.strip()
            company_name = company_tag.text.strip()
            job_link = "https://remoteok.io" + link_tag["href"]

            jobs.append([job_title, company_name, job_link])

    return jobs

def save_to_csv(jobs):
    """Save job listings to a CSV file"""
    with open("jobs.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Job Title", "Company", "Link"])
        writer.writerows(jobs)
    print(f"Saved {len(jobs)} jobs to jobs.csv")

if __name__ == "__main__":
    jobs = fetch_jobs()
    if jobs:
        save_to_csv(jobs)
    else:
        print("No jobs found.")
