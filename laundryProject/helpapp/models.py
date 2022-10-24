# from pyexpat import model
# from django.db import models

# class User(models.Model):
#     user_id = models.AutoField(max_length=10, primary_key=True)
#     user_name = models.CharField(max_length=255, null=False)
#     password = models.CharField(max_length=255, null=False)
#     user_icon = models.CharField(max_length=255)

# class Cabinets(models.Model):
#     loundry_id = models.AutoField(max_length=10, primary_key=True)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Cabinet(models.Model):
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.PROTECT,
    )
    laundry_tag = models.CharField(max_length=255)
    image = models.ImageField(upload_to='img/', default='static/upload_img/img/image.jpg')
    memo = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.author)