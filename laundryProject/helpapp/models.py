from datetime import date
from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
#トロフィーのきのうつけるなら
# class Award(models.Model):
#     name = models.CharField(max_length=255)
#     text = models.CharField(max_length=255)
#     def __str__(self):
#         return self.name

# class Winned_Award(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#     )
#     award = models.ForeignKey(
#         Award, 
#         on_delete=models.PROTECT,
#     )
#     date =

#     def __str__(self):
#         return self.user

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
    image = models.ImageField(upload_to='icon/', default='static/upload_img/icon/image.jpg')

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
