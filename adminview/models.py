from django.db import models
from django.contrib.auth.models import User
from homepage.models import UserProfile
from django.utils import timezone

class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
