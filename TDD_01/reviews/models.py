from django.contrib.auth import get_user_model
from django.db import models

from utils.models import BaseModel
from restaurants.models import Restaurant

User = get_user_model()

# Create your models here.
class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    comment= models.TextField()
