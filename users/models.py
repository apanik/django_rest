from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Permissons(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100)
    permissons = models.ManyToManyField(Permissons)

    def __str__(self):
        return self.name

class User(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200,unique = True)
    password =  models.CharField(max_length=200)
    username = models.CharField(max_length=200,unique=True)
    role = models.ForeignKey(Role,on_delete=models.SET_NULL,null=True)


    USERNAME_FILED = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
