from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    password = models.CharField(max_length=128, default=None, null=True)
    age = models.IntegerField()
    resume = models.FileField(upload_to='media/')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=None)
    education_course_name = models.CharField(max_length=200, null=True, blank=True)
    certifications = models.TextField(max_length=1000, null=True, blank=True)  # Store certifications as text
    most_recent_job = models.CharField(max_length=100, null=True, blank=True)
    linkedin_url = models.CharField(max_length=300, null=True, blank=True)
    Applying_For = models.CharField(max_length=100, null=True, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    previous_company = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.user.username  # Assuming 'username' is a field of the User model
