import requests
from bs4 import BeautifulSoup
from store.models import Job
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        api_key = 'DIE4AXGWO8GY6YYRJX84UM1CWFY9XBIJFGHEMQU7DULSAWXSLVJQDRVBKIBORNB7T7DBMY2J9OKXBNDO'
        
        job_list = ['python Developer',
                    
                    ]
        
        for job_name in job_list:
            indeed_url = f"https://pk.indeed.com/jobs?q={job_name.replace(' ', '+')}"
            scrapingbee_url = f"https://app.scrapingbee.com/api/v1/?api_key={api_key}&url={indeed_url}"
            print("scrapin url_______",scrapingbee_url)
            response = requests.get(scrapingbee_url,headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/83.0.4103.116 Safari/537.36"
        })
            print(response.status_code)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                #print("soup__________",soup)

                
                jobs_container = soup.find('div', class_='mosaic mosaic-provider-jobcards mosaic-provider-hydrated')
                if jobs_container:
                    job_listings = jobs_container.find('ul', class_=['css-zu9cdh', 'eu4oa1w0'])
                    if job_listings:
                        jobs = job_listings.find_all('li')
                        print(jobs)
                
                

            #     for job in jobs:
            #         job_link = job.find('div', class_='css-dekpa e37uo190')
            #         if job_link:  
            #             job_found = job_link.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0')
            #             if job_found:
            #                 title_span = job_found.find('span')
            #                 if title_span:
            #                     title_tag = title_span.text.strip()
            #                     print(f"Job Title: {title_tag}")

            #                     if any(title_tag.lower() in title.lower() for title in job_list):
            #                         lead_url = "https://pk.indeed.com" + job_found['href']  # Use job_found to get href
            #                         company = job.find('span', class_=['css-63koeb', 'eu4oa1w0']).text.strip() if job.find('span', class_=['css-63koeb', 'eu4oa1w0']) else 'Unknown'
            #                         print(f"Company: {company}")

            #                         location = job.find('div', class_='css-1p0sjhy eu4oa1w0').text.strip() if job.find('div', class_='css-1p0sjhy eu4oa1w0') else 'Not specified'
            #                         job_type = job.find('li').text.strip() if job.find('li') else 'Not specified'

            #                         # Check if the job already exists in the database
            #                         if not Job.objects.filter(title__iexact=title_tag).exists():
            #                             Job.objects.create(
            #                                 title=title_tag,
            #                                 company=company,
            #                                 location=location,
            #                                 job_type=job_type,
            #                                 lead_url=lead_url
            #                             )
            #                             print(f"Saved job: {title_tag}")
            #                         else:
            #                             print(f"Job already exists: {title_tag} at {company}")
            #                     else:
            #                         print(f"Job title '{title_tag}' is not in the specified list.")
            #                 else:
            #                     print("No span tag found for job title.")
            #             else:
            #                 print("No anchor tag found for job title.")
            #         else:
            #             print("No div tag found for job link.")
            # else:
            #     print("Failed to retrieve content from ScrapingBee.")
