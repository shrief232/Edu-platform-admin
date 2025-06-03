from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    language_preference = models.CharField(max_length=10, choices=[('en', 'English'), ('ar', 'Arabic')], default='en')
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True, null=True, region='EG') 
    company_name = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    def __str__(self):
        return self.email


class EmailVerification(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='email_verification')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.email} - {self.otp_code}"