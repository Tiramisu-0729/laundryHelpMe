from pyexpat import model
from django.db import models

class User(models.Model):
    user_id = models.AutoField(max_length=10, primary_key=True)
    user_name = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    user_icon = models.CharField(max_length=255)

class Cabinets(models.Model):
    loundry_id = models.AutoField(max_length=10, primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    