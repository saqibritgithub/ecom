# Generated by Django 5.1.1 on 2024-10-03 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_rename_job_jobs'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Jobs',
            new_name='Job',
        ),
    ]
