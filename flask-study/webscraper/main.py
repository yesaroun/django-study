from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from selenium import webdriver
import os

def get_page_count(keyword):
    path = os.getcwd() + "/chromedriver"
    browser = webdriver.Chrome(path)

    base_url = "https://kr.indeed.com/jobs?q="

    browser.get(f"{base_url}{keyword}")

    response = browser.page_source

    results = []
    soup = BeautifulSoup(response, "html.parser")
    pagination = soup.find("ul", class_="pagination-list")
    if pagination is None:
        return 1
    pages = pagination.find_all("li", recursive=False)
    print(len(pages))

get_page_count("python")


def extract_indeed_job(keyword):
    path = os.getcwd() + "/chromedriver"
    browser = webdriver.Chrome(path)

    base_url = "https://kr.indeed.com/jobs?q="

    browser.get(f"{base_url}{keyword}")

    response = browser.page_source

    results = []
    soup = BeautifulSoup(response, "html.parser")
    # print(soup)
    job_list = soup.find("ul", class_="jobsearch-ResultsList")
    jobs = job_list.find_all('li', recursive=False)     # recursive=False : ul 바로 아래의 li 태그만!
    # print(len(jobs))
    for job in jobs:
        # print(job)
        zone = job.find("div", class_="mosaic-zone")
        if zone is None:
            anchor = job.select_one("h2 a")
            # print(anchor)
            # print("-"*20)
            title = anchor["aria-label"]
            link = anchor["href"]
            # print(title, link)
            # print('-'*20)
            company = job.find("span", class_="companyName")
            location = job.find("div", class_="companyLocation")
            job_data = {
                'link': f"https://kr.indeed.com{link}",
                'company': company.string,
                'location': location.string,
                'position': title
            }
            results.append(job_data)
    for result in results:
        print(result, "\n --------------------")






