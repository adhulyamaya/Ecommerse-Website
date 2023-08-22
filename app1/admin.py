from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class ColorAdmin(admin.ModelAdmin):
    list_display = ['color']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['username',"variant"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
  

class VariantAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'variant', 'Product', 'Color', 'Size']


class CartAdmin(admin.ModelAdmin):
    list_display = ['id','username','variant','quantity']  

class AddressAdmin(admin.ModelAdmin):
    list_display = ['id','username','flat','locality','city'] 

class BrandAdmin(admin.ModelAdmin):
    list_display = ['id','brand']  
class CouponAdmin(admin.ModelAdmin):
    list_display = ['id','name']  


admin.site.register(custom_user)
admin.site.register(category)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variant,VariantAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Wishlist)
admin.site.register(Brand)
admin.site.register(Coupon)
admin.site.register(Offer)
