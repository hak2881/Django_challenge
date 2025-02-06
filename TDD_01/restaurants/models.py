from django.db import models

from utils.models import BaseModel


# Create your models here.

class Restaurant(BaseModel):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=50)
    open_time = models.TimeField(null=True,blank=True)
    close_time = models.TimeField(null=True,blank=True)
    last_order = models.TimeField(null=True,blank=True)
    regular_holiday = models.CharField(choices=DAYS_OF_WEEK, max_length=20, null=True,blank=True)