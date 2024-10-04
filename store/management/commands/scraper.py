import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from datetime import datetime, date
from store.models import Job


class Command(BaseCommand):
    help = 'Scrapes job listings from python.org and saves them into the database.'

    def handle(self, *args, **kwargs):
        url = "https://www.python.org/jobs/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        jobs = soup.find('ol', class_='list-recent-jobs').find_all('li')

        for job in jobs:
            try:
                
                job_link = job.find('a')
                title = job_link.text.strip()
                job_url = job_link['href'].strip()  

                company_tag = job.find('span', class_='listing-company-name')
                company_name = company_tag.contents[-1].strip()

                location = job.find('span', class_='listing-location').text.strip()

                job_type_tag = job.find('span', class_='listing-job-type')
                job_type = ', '.join([t.text.strip() for t in job_type_tag.find_all('a')])

                date_posted_text = job.find('span', class_='listing-posted').find('time').text.strip()
                date_posted = datetime.strptime(date_posted_text, '%d %B %Y').date()

                lead_date = date.today()
                platform = 'Python.org'
                lead_url = url
                company_url = url
                posted_date = date_posted
                region = location
                industry = 'Software'

                
                job_exists = Job.objects.filter(lead_url=job_url).exists()

                if not job_exists:
                    Job.objects.create(
                        title=title,
                        company=company_name,
                        location=location,
                        job_type=job_type,
                        date_posted=date_posted,
                        lead_date=lead_date,
                        platform=platform,
                        lead_url=job_url,  # Use job_url as the lead_url here
                        company_url=company_url,
                        posted_date=posted_date,
                        region=region,
                        industry=industry,
                        validated=False,
                        company_url_validated=False,
                        already_exist_validated=False,
                        invalid_title_validated=False,
                        email_validated=False,
                        posted_date_formatted=posted_date.strftime('%Y-%m-%d') if posted_date else None
                    )

                    self.stdout.write(self.style.SUCCESS(f"Job '{title}' saved successfully."))
                else:
                    self.stdout.write(self.style.WARNING(f"Job '{title}' already exists in the database (URL: {job_url})."))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing job '{title}': {e}"))

