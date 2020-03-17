from django.db import models
from django.contrib.auth.models import AbstractUser

DISCIPLINES_AREAS = (
    ('1', 'Programming - C++'),
    ('2', 'Programming - Python'),
    ('3', 'Game Development'),
    ('4', 'Data Structures and Algorithms'),
    ('5', 'Computer Organization'),
    ('6', 'Operating Systems'),
    ('7', 'Programming Languages'),
    ('8', 'Cybersecurity'),
    ('9', 'Mobile Applications'),
    ('10', 'Artificial Intelligence'),
    ('11', 'Networks'),
    ('12', 'Theory of Computation'),
    ('13', 'Parallel and Distributed Systems'),
)

MEETING_DAYS = (
    ('MW', 'Monday and Wednesday'),
    ('TR', 'Tuesday and Thursday'),
)
MAX_CLASSES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
)

YES_NO = (
    ('no', 'no'),
    ('yes', 'yes'),
)


# Create your models here.
class BaseUser(AbstractUser):
    user_type = models.CharField(max_length=128, blank=True, null=True)
    sec_question1 = models.CharField(max_length=128, blank=True, null=True)
    sec_question2 = models.CharField(max_length=128, blank=True, null=True)
    isApproved = models.CharField(max_length=128, choices=YES_NO, default=YES_NO[1][1])


class Class(models.Model):
    course_number = models.CharField(max_length=128, blank=True, null=True)
    course_id = models.CharField(max_length=128, blank=True, null=True)
    meeting_days = models.CharField(max_length=128, choices=MEETING_DAYS, blank=True, null=True)
    disciplines_areas = models.CharField(max_length=128, choices=DISCIPLINES_AREAS, blank=True, null=True)


class Instructor(models.Model):
    last_name = models.CharField(max_length=128, blank=True, null=True)
    maximum_class_load = models.CharField(max_length=128, choices=MAX_CLASSES, blank=True, null=True)
    disciplines_areas = models.CharField(max_length=128, choices=DISCIPLINES_AREAS, blank=True, null=True)
