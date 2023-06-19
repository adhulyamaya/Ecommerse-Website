   
from django.db import models

class custom_user(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    is_superuser = models.BooleanField(default=False)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    status =  models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Product(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=20)
    category = models.CharField(max_length=100)
    description = models.TextField()
    product_image = models.ImageField(upload_to='products',default='default_image.jpg')

    def __str__(self):
        return self.name
    
class category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to='category',default='default_image.jpg')

    def __str__(self):
        return self.name    


