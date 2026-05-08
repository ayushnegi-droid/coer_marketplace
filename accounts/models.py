from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Profile(models.Model):
    YEAR_CHOICES = ['1st Year', '2nd Year', '3rd Year', '4th Year', 'Post-Grad']

    user       = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    full_name  = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True)
    year       = models.CharField(max_length=20, blank=True)
    bio        = models.TextField(blank=True)
    picture    = models.ImageField(upload_to='profiles/', blank=True, null=True)
    setup_done = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
