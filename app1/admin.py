from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import custom_user, category, Product, Color, Size, Variant


class ColorAdmin(admin.ModelAdmin):
    list_display = ['color']

    # def color_tag(self, obj):
    #     if obj.code is not None:
    #         return mark_safe('<p style="background-color:{}">Color</p>'.format(obj.code))
    #     else:
    #         return ""

    # color_tag.short_description = 'Color Tag'


class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1
    show_change_link = True
    readonly_fields = ['product_image_tag']

    def product_image_tag(self, instance):
        return '<img src="%s" width="50" height="50" />' % instance.Product.product_image.url

    product_image_tag.allow_tags = True
    product_image_tag.short_description = 'Product Image'


# class ImagesInline(admin.StackedInline):
#     model = Images
#     extra = 1



class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    # inlines = [ImagesInline, VariantInline]

    # def display_product_image(self, obj):
    #     return mark_safe(f'<img src="{obj.product_image.url}" width="50" height="50" />')

    # display_product_image.short_description = 'Product Image'


class VariantAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'variant', 'Product', 'Color', 'Size']







class ImagesAdmin(admin.ModelAdmin):
    list_display = [ 'display_image']

    def display_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')

    display_image.short_description = 'Product Image'



admin.site.register(custom_user)
admin.site.register(category)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
# admin.site.register(Images, ImagesAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variant,VariantAdmin)


