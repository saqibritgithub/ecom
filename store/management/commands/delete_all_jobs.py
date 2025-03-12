from django.core.management.base import BaseCommand
from store.models import Job

class Command(BaseCommand):
    help = 'Delete all jobs from the database'

    def handle(self, *args, **kwargs):
        # Confirm deletion
        confirm = input("Are you sure you want to delete all jobs? (yes/no): ")
        if confirm.lower() == 'yes':
            Job.objects.all().delete()  # Delete all jobs
            self.stdout.write(self.style.SUCCESS('Successfully deleted all jobs.'))
        else:
            self.stdout.write(self.style.WARNING('Deletion cancelled.'))