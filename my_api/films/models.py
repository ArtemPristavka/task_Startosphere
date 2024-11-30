from django.db import models
from django.contrib.auth.models import User


class Film(models.Model):
    "Модель фильма"
    
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    user = models.ManyToManyField(User, related_name="films")
