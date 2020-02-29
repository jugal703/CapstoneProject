from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class BaseUser(AbstractUser):
    user_type = models.CharField(max_length=128, blank=True, null=True)
    sec_question1 = models.CharField(max_length=128, blank=True, null=True)
    sec_question2 = models.CharField(max_length=128, blank=True, null=True)

