import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self,*args, **kwargs):
        web = requests.get("https://www.tutorialsfreak.com/")
        print(web.status_code)          
        soup = BeautifulSoup(web.content,"html.parser")
        data = soup.find('div', class_= 'banner-heading-wrapper')
       # print(data.find_all('h1'))
        des = (soup.find('h1',{"class":"main-heading my-3"}))
        print(des.string)
        lines = soup.find_all('p')
        # for l in lines:
        #     print(l.text)

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from store.models import Job
from datetime import datetime, timedelta

def handle_date(date_string):
    today = datetime.today()
    if "yesterday" in date_string.lower():
        return (today - timedelta(days=1)).date()
    if "days ago" in date_string.lower():
        days_ago = int(date_string.split()[0])
        return (today - timedelta(days=days_ago)).date()
    if "weeks ago" in date_string.lower():
        weeks_ago = int(date_string.split()[0])
        return (today - timedelta(weeks=weeks_ago)).date()

    try:
        return datetime.strptime(date_string, '%d %B').replace(year=today.year).date()
    except ValueError:
        return None

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        page_number = 2
        
        while True:
            url = f"https://www.reed.co.uk/jobs/web-developer-jobs?pageno={page_number}"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            main_section = soup.find('main', class_="search-results_hide__9cTQ5 search-results_mainBlock__Rp2r_ order-2 col-sm-12 col-md-8 col-lg-7")
            if main_section is None:
                print(f"No jobs found on page {page_number} Stopping the scraper.")
                break

            jobs=main_section.find_all('div', class_="job-card_jobCard__body__86jgk card-body")

            for job in jobs:
                title_tag = job.find('h2', class_="job-card_jobResultHeading__title__IQ8iT")
                title = title_tag.find('a').get_text()
                job_id = None
                anchor_tag = job.find_all('a', class_='job-card_jobTitle__HORxw')

                for anchor_id in anchor_tag:
                    job_id = anchor_id.get('data-id')

                company = job.find('a', class_="job-card_profileUrl__fRi56 gtmJobListingPostedBy").get_text()
                date_post = job.find('div', class_="job-card_jobResultHeading__postedBy__sK_25").get_text()
                date_posted_text = date_post.split('by')[0].strip()
                date_posted = handle_date(date_posted_text)

                ul_tag = job.find('ul', class_='job-card_jobMetadata__gjkG3')

                if ul_tag:
                    salary = ul_tag.find_all('li')[0].get_text().strip()
                    location_tag = ul_tag.find('li', attrs={'data-qa': 'job-card-location'})
                    location = location_tag.get_text().strip() if location_tag else 'Location not found'
                    job_type = ul_tag.find_all('li', class_="job-card_jobMetadata__item___QNud list-group-item")[2].get_text().strip()  # Third li tag is job type

                    company = company.strip()
                    title = title.strip()
                    if not Job.objects.filter(job_id=job_id).exists():
                        Job.objects.create(
                            job=job_id,
                            title=title,
                            company=company,
                            location=location,
                            job_type=job_type,
                            salary=salary,
                            date_posted=date_posted,
                        )
                        print(f"Saved job {title}")
                    else:
                        print(f"Job already exists: {title} at {company}")

            next_button = soup.find_all('a', class_='page-link next')
        
            if next_button:
                page_number += 1
                print(f"Moving to page {page_number}")
            else:
                print("No more pages. Stopping the scraper.")
                break


import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from store.models import Job
from datetime import datetime, timedelta

def handle_date(date_string):
    today = datetime.today()
    if "yesterday" in date_string.lower():
        return (today - timedelta(days=1)).date()
    if "days ago" in date_string.lower():
        days_ago = int(date_string.split()[0])
        return (today - timedelta(days=days_ago)).date()
    if "weeks ago" in date_string.lower():
        weeks_ago = int(date_string.split()[0])
        return (today - timedelta(weeks=weeks_ago)).date()

    try:
        return datetime.strptime(date_string, '%d %B').replace(year=today.year).date()
    except ValueError:
        return None

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for i in range(1,54):
        
       
            url = f"https://www.reed.co.uk/jobs/web-developer-jobs?pageno={i}"
            response = requests.get(url)
            print(response.status_code)
            soup = BeautifulSoup(response.content, "html.parser")
            main_section = soup.find('main', class_="search-results_hide__9cTQ5 search-results_mainBlock__Rp2r_ order-2 col-sm-12 col-md-8 col-lg-7")
            

            jobs=main_section.find_all('div', class_="job-card_jobCard__body__86jgk card-body")

            for job in jobs:
                title_tag = job.find('h2', class_="job-card_jobResultHeading__title__IQ8iT")
                title = title_tag.find('a').get_text()
                job_id = None
                anchor_tag = job.find_all('a', class_='job-card_jobTitle__HORxw')

                for anchor_id in anchor_tag:
                    job_id = anchor_id.get('data-id')
                    #print(f"Scraping job ID: {job_id}, Title: {title}")

                company = job.find('a', class_="job-card_profileUrl__fRi56 gtmJobListingPostedBy").get_text()
                date_post = job.find('div', class_="job-card_jobResultHeading__postedBy__sK_25").get_text()
                date_posted_text = date_post.split('by')[0].strip()
                date_posted = handle_date(date_posted_text)

                ul_tag = job.find('ul', class_='job-card_jobMetadata__gjkG3')

                if ul_tag:
                    salary = ul_tag.find_all('li')[0].get_text().strip()
                    location_tag = ul_tag.find('li', attrs={'data-qa': 'job-card-location'})
                    location = location_tag.get_text().strip() if location_tag else 'Location not found'
                    job_type = ul_tag.find_all('li', class_="job-card_jobMetadata__item___QNud list-group-item")[2].get_text().strip()  # Third li tag is job type

                    company = company.strip()
                    title = title.strip()
                    if not Job.objects.filter(job_id=job_id).exists():
                        Job.objects.create(
                            job_id=job_id,
                            title=title,
                            company=company,
                            location=location,
                            job_type=job_type,
                            salary=salary,
                            date_posted=date_posted,
                        )
                        print(f"Saved job {title}")
                    else:
                        print(f"Job already exists: {title} at {company}")

            # next_button = soup.find_all('a', class_='page-link next')
        
            # if next_button:
            #     page_number += 1
            #     print(f"Moving to page {page_number}")
            # else:
            #     print("No more pages. Stopping the scraper.")
            #     break
