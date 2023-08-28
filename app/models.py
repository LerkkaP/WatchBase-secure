from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Watch(models.Model):
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
