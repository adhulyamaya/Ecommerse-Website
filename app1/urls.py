from django.urls import path
from . import views
# urls.py

from django.conf import settings
from django.conf.urls.static import static

# ... other URL patterns ...




urlpatterns = [
   
   
    path('user_login/', views.user_login, name='user_login'),
    path('admin_login/', views.admin_login, name='adminlogin'),
    path("admin_logout/",views.admin_logout,name="admin_logout"),
    path('', views.user_home, name='userhome'),

    path('home_before/', views.home_before, name='home_before'),

    path('products/',views.products, name='products'),
    path('shop_before/',views.shop_before, name='shop_before'),
    path('shop/',views.shop, name='shop'),

    path('signup/', views.signup, name='signup'),
    path('otplogin/', views.otplogin, name='otplogin'),
    # path('otplogin/<str:otp>/', views.otplogin, name='otplogin'),
    path('otp_grn/', views.otp_grn, name='otp_grn'),
    path('logout', views.user_logout, name='logout'),
    path('user_product/<int:Category_id>/', views.user_product, name='user_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('admin_home', views.admin_home, name='adminhome'),
    path('product/<int:product_id>/variant_detail/<int:variant_id>/', views.variant_detail, name="variant_detail"),
    path('product/<int:product_id>/variant_detail/<int:variant_id>/', views.variant_detail, name="variant_detail"),
    # path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('show-cart', views.show_cart, name='show-cart'),
    path('cart_inc/<int:item_id>', views.cart_inc, name='cart_inc'),
    path('cart_dec/<int:item_id>', views.cart_dec, name='cart_dec'),
    path('checkout', views.checkout, name='checkout'),
    path('cart_remove/<int:item_id>',views.cart_remove,name = 'cart_remove'),
    path('shop',views.shop,name = 'shop'),
    path('user_profile',views.user_profile,name = 'user_profile'),
    path('user_address/',views.user_address, name='user_address'),
    path('user_proeditadd/<int:address_id>', views.user_proeditadd, name='user_proeditadd'),
    # path('user_proeditadd/', views.user_proeditadd, name='user_proeditadd'),
    path('ordersuccess/',views.ordersuccess,name = 'ordersuccess'),
    path('contact/',views.contact,name ='contact'),
    path('about/',views.about,name ='about'),
    path('wishlist/',views.wishlist,name ='wishlist'),
    path('search_products/', views.search_products, name='search_products'),

    path('add_to_wishlist/',views.add_to_wishlist,name ='add_to_wishlist'),
    path('wishlist_remove/<int:item_id>',views.wishlist_remove,name = 'wishlist_remove'),
    path('view_order/',views.view_order,name = 'view_order'),
    path('order_history/',views.order_history,name = 'order_history'),
    path('product/<int:product_id>/variant/<int:variant_id>/', views.variant_detail, name='variant_detail'),
    path('changepassword/',views.changepassword,name = 'changepassword'),


    
    path('admin_user/', views.admin_user, name='admin_user'),
    path('products/',views.products, name='products'),
    path('admin_variant/',views.admin_variant, name='admin_variant'),
    path('orderadmin/',views.orderadmin, name='orderadmin'),
    path("order_items/<int:order_id>",views.order_items,name = 'order_items'),
    path('category/', views.category_view, name='category'),
    path("add_category/",views.add_category,name = 'add_category'),
    path("add_product/",views.add_product,name = 'add_product'),
    
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    # path('update_category/<int:category_id>/', views.update_category, name='update_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('admin_user/<int:user_id>/', views.block_unblock_user, name='block_unblock_user'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/',views.delete_product, name='delete_product'),
    path('color_admin',views.color_admin, name='color_admin'),

    path('size_admin',views.size_admin, name='size_admin'),

    
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
