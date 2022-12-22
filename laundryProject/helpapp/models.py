from datetime import date
from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Report(models.Model):
    image = models.CharField(max_length=255)
    ai_result = models.CharField(max_length=255)
    user_result = models.CharField(max_length=255)
    def __str__(self):
        return str(self.id)


class Cabinet(models.Model):
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.PROTECT,
    )
    name = models.CharField(max_length=255)
    laundry_tag = models.CharField(max_length=255)
    image = models.ImageField(upload_to='img/', default='static/upload_img/img/image.jpg')
    memo = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return str(self.author)

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to='icon/', blank=True, null=True)
    judge_cnt = models.IntegerField(default=0)
    washer_cnt = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.user)

class Washer_log(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

class Laundry(models.Model):
    washer_log_id = models.ForeignKey(
        Washer_log,
        on_delete=models.CASCADE,
        related_name='washer_log_id'
    )
    cabinet_id = models.ForeignKey(
        Cabinet,
        on_delete=models.CASCADE,
        related_name='cabinet_id'
    )
    def __str__(self):
        return str(self.washer_log_id)
