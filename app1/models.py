
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
    
class Brand(models.Model):
    brand = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.id} - {self.brand}" 
    
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
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

class Coupon(models.Model):
    coupon_code= models.CharField(max_length=100 ,blank=True,null = True)
    is_expired = models.BooleanField(default=False)
    discount_price= models.DecimalField(max_digits=10,decimal_places=2,default=0)
    minimum_amount = models.IntegerField(default=500)
    
    def __str__(self):
        return self.coupon_code

    
class Cart(models.Model):
    username = models.ForeignKey(custom_user,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL,null=True,blank= True)
    discount_price= models.DecimalField(max_digits=10,decimal_places=2,default=0)
    quantity = models.PositiveIntegerField(default=1)
    
    def total_cost(self):
        return self.quantity * self.variant.price  

class Wishlist(models.Model):
    username = models.ForeignKey(custom_user,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant,on_delete=models.CASCADE)
   
   
class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('order pending','order pending'),
        ('order confirmed','order confirmed'),
        ('delivered','delivered'),
        ('returned','returned'),
        ('cancelled','cancelled')
    )

    PAYMENT_CHOICES = (
        ('cash on delivery','cash on delivery'),
        ('online payment','online payment')
    )

    customer = models.ForeignKey(custom_user,on_delete=models.SET_NULL,null=True,blank=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=100,choices=ORDER_STATUS_CHOICES,default='order pending')
    payment_type = models.CharField(max_length=100,choices=PAYMENT_CHOICES,default='cash on delivery')
    total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL,null=True,blank= True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.order_status}"
   


class OrderItems(models.Model):
    variant = models.ForeignKey(Variant,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    

    def __str__(self):
        return f"OrderItem #{self.id}"
    

class Wallet(models.Model):
    user=models.ForeignKey(custom_user,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):  
        return self.user 


