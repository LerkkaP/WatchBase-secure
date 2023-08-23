from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.username

class Watch(models.Model):
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
