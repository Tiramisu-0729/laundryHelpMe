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
    name = models.CharField(max_length=255)
    laundry_tag = models.CharField(max_length=255)
    image = models.ImageField(upload_to='img/', default='static/upload_img/img/image.jpg')
    memo = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.author)