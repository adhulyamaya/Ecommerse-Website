   
from django.db import models
from django.utils.safestring import mark_safe
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
    

class Address(models.Model):
    username = models.ForeignKey(custom_user, on_delete=models.CASCADE)
    flat = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=255)

    def __str__(self):
        return self.flat







class category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to='category',default='default_image.jpg')

    def __str__(self):
        return self.name  


class Color(models.Model): 
    color = models.CharField(max_length=50)
    def __str__(self):
        return self.color
    

class Size(models.Model):
    size = models.CharField(max_length=20)
    
    def __str__(self):
        return self.size
    
class Product(models.Model):
    VARIANTS = (('None','None'),('Size','Size'),('Color','Color'),('Size-Color','Size-Color'))

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    description = models.TextField()
    sales_count = models.PositiveIntegerField(default=0)
    wardrobe_essential = models.BooleanField(default=False)
    image = models.ImageField(blank=True, upload_to='images/') 
 
    def __str__(self):
        return self.name


class Variant(models.Model):
    id = models.AutoField(primary_key=True)
    variant = models.CharField(max_length=100,blank= True,null= True)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Color = models.ForeignKey(Color,on_delete=models.CASCADE)
    Size = models.ForeignKey(Size,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0) 
    image1 = models.ImageField(blank=True, upload_to='images/') 
    image2 = models.ImageField(blank=True, upload_to='images/') 
    image3 = models.ImageField(blank=True, upload_to='images/') 
    image4 = models.ImageField(blank=True, upload_to='images/') 
    def __str__(self):
        return self.variant

   

    
class Cart(models.Model):
    username = models.ForeignKey(custom_user,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
   

    def total_cost(self):
        return self.quantity * self.variant.price

    



class Banner(models.Model):
    image = models.ImageField(upload_to='banners')
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    
 


