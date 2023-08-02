from django.db import models
from django.contrib.auth.models import User

class Education(models.Model):
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    completion_year = models.IntegerField()

class Certification(models.Model):
    name = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()

class CertificationFile(models.Model):
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE)
    file = models.FileField(upload_to='certification_files/')

class Job(models.Model):
    title = models.CharField(max_length=100)

class PreviousJob(models.Model):
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    age = models.IntegerField()
    resume = models.FileField(upload_to='media/')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=None)

    highest_education = models.ManyToManyField(Education, blank=True)
    certifications = models.ManyToManyField(Certification, blank=True)
    certification_files = models.ManyToManyField(CertificationFile, blank=True)
    job_applying_for = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    previously_employed_job = models.ForeignKey(PreviousJob, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name