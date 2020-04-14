from django.db import models
from django.contrib.auth.models import AbstractUser

DISCIPLINES_AREAS = (
    ('Programming - C++', 'Programming - C++'),
    ('Programming - Python', 'Programming - Python'),
    ('Game Development', 'Game Development'),
    ('Data Structures and Algorithms', 'Data Structures and Algorithms'),
    ('Computer Organization', 'Computer Organization'),
    ('Operating Systems', 'Operating Systems'),
    ('Programming Languages', 'Programming Languages'),
    ('Cybersecurity', 'Cybersecurity'),
    ('Mobile Applications', 'Mobile Applications'),
    ('Artificial Intelligence', 'Artificial Intelligence'),
    ('Networks', 'Networks'),
    ('Theory of Computation', 'Theory of Computation'),
    ('Parallel and Distributed Systems', 'Parallel and Distributed Systems'),
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
    assigned_instructor = models.CharField(max_length=128, default='No Instructor')
    course_number = models.CharField(max_length=128, blank=True, null=True)
    course_title = models.CharField(max_length=128, blank=True, null=True)
    meeting_days = models.CharField(max_length=128, choices=MEETING_DAYS, blank=True, null=True)
    start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    disciplines_area = models.ManyToManyField('DisciplinesAreas')

    def __str__(self):
        return self.course_number


class Instructor(models.Model):
    instructor_id = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    maximum_class_load = models.CharField(max_length=128, choices=MAX_CLASSES, blank=True, null=True)
    disciplines_area = models.ManyToManyField('DisciplinesAreas')

    def __str__(self):
        return self.instructor_id


class DisciplinesAreas(models.Model):
    disciplines_area = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.disciplines_area
