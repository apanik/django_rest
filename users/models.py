from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200,unique = True)
    password =  models.CharField(max_length=200)
    username = models.CharField(max_length=200,unique=True)

    USERNAME_FILED = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name.capitalize()  + '   ' + self.last_name.capitalize()
