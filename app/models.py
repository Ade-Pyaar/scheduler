from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser


# sauce code: 243536



class MyUsers(AbstractUser):
    email = models.EmailField("Email", max_length=100, unique=True)
    email_service = models.BooleanField("Email Service", default=False)
    # email_listing = models.OneToOneField("EmailListing", on_delete=models.CASCADE, blank=True, null=True)
    email_listing = models.JSONField("Email Listing", default=dict, blank=True)







