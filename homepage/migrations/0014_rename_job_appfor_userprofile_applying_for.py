# Generated by Django 4.2.3 on 2023-08-07 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0013_userprofile_previous_company_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='job_appfor',
            new_name='Applying_For',
        ),
    ]
