from django.urls import path
from . import views
# urls.py

from django.conf import settings
from django.conf.urls.static import static

# ... other URL patterns ...




urlpatterns = [
   
   
    path('', views.user_login, name='user_login'),
    path('admin_login', views.admin_login, name='adminlogin'),
    path('user_home', views.user_home, name='userhome'),
    path('signup', views.signup, name='signup'),
    path('otplogin', views.otplogin, name='otplogin'),
    # path('otplogin/<str:otp>/', views.otplogin, name='otplogin'),
    path('otp_grn/', views.otp_grn, name='otp_grn'),
    path('logout', views.user_logout, name='logout'),
    path('user_product/<int:Category_id>/', views.user_product, name='user_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('admin_home', views.admin_home, name='adminhome'),
   



    
    

    
    path('admin_user/', views.admin_user, name='admin_user'),
    path('products',views.products, name='products'),
    path('category/', views.category_view, name='category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('admin_user/<int:user_id>/', views.block_unblock_user, name='block_unblock_user'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/',views.delete_product, name='delete_product'),

    
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
