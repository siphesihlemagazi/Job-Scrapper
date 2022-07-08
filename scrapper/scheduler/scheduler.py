import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
from job_scrapper.settings import DOMAIN, JOB_SITE_DOMAIN, JOB_SITE_SEARCH
import logging


def extract_jr_python_software_developer_jobs(url):
    data = []
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    jobs = soup.find_all('div', class_='job_seen_beacon')

    for job in jobs:

        job_title = job.find('h2', class_='jobTitle')

        filters = ['Junior', 'Junior Python Developer', 'Junior Software Developer']

        for filter in filters:
            if filter in job_title.text:
                data.append(
                    {
                        "title": job_title.text,
                        "uuid": job_title.a.get('id'),
                        "location": job.find('div',
                                             class_='companyLocation').text,
                        "date_posted": job.find('span', class_='date').text,
                        "link": JOB_SITE_DOMAIN + job_title.a.get(
                            'href'),
                        "description": job.find('div',
                                                class_='job-snippet').text,
                    }
                )

    return data


def post_jobs():
    endpoint = DOMAIN + '/jobs/'
    website_url = JOB_SITE_DOMAIN + JOB_SITE_SEARCH

    for job in extract_jr_python_software_developer_jobs(website_url):
        
        response = requests.post(endpoint, json=job)
        if str(response.status_code) == "201":
            logging.info(f"{response.status_code}: Successfully posted job")

        elif str(response.status_code) == "400":
            logging.warning(f"{response.status_code}: Job with this uuid "
                            f"already exists")

            logging.info("Trying to update job...")
            response = requests.put(endpoint + job['uuid'], json=job)
            if str(response.status_code) == "200":
                logging.info(f"{response.status_code}: Successfully updated job")
        else:
            logging.critical(f"{response.status_code}: Unknown error")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(post_jobs, "interval", minutes=1, id="jobs_001",
                      replace_existing=True)
    scheduler.start()
