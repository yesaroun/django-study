from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="

    response = get(f"{base_url}{keyword}")
    if response.status_code != 200:
        print("can't request website")
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("section", class_="jobs")
        # print("jobs start------------")
        # print(jobs)
        # print("-----------jobs end")
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            # print("job_posts***************")
            # print(job_posts)
            # print("end job_posts___________")
            # print("job_posts-------")     # <li class="view-all"> except
            job_posts.pop(-1)
            for post in job_posts:
                # print(post)
                # print("/"*20)
                anchors = post.find_all('a')
                # print("find_all : \t", anchors)
                # print("-"*20)
                # print(post['class'])

                # 혹시 버튼 요소(view-all) 일 경우 처리 코드(앞에서 pop(-1)로 처리 했었긴 하다)
                if post['class'] == ['view-all']:
                    # print(3)
                    break
                anchors = anchors[1]
                # print("[1] : \t", anchors)
                # print("-"*20)
                link = anchors['href']
                company, kind, region = anchors.find_all('span', class_="company")
                title = anchors.find('span', class_='title')
                # print(company.string, kind.string, region.string, title.string)
                job_data = {
                    'link': f"https://weworkremotely.com{link}",
                    'company': company.string,
                    'location': region.string,
                    'position': title.string
                }
                results.append(job_data)
            # print(results)
            # for result in results:
            #     print(result)
            #     print("/" * 20)
        return results
