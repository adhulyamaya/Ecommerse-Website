from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import custom_user,Product
from django.contrib.auth.models import User

from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from .models import *

import re
import random,vonage
from vonage import Sms

client=vonage.Client(key="23594a08",secret="asBI3u5U6nnRnMd6")
sms=vonage.Sms(client)



@never_cache
def user_login(request):
    if 'username' in request.session:
        username = request.session['username']
        user = custom_user.objects.get(username=username)

        if not user.is_superuser:
            return redirect('userhome')
        else:
            return redirect('adminhome')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username.strip() or not password.strip():
            return render(request, 'user_login.html', {'user404': 'Wrong credentials'})

        try:
            user = custom_user.objects.get(username=username, password=password)

            if user is not None:
                if not user.is_superuser:
                    if user.status:
                        request.session['username'] = username
                        return redirect('userhome')
                    else:
                        return render(request, 'user_login.html', {'user404': 'Wrong credentials'})
                else:
                    return render(request, 'user_login.html', {'user404': 'Please use admin login'})

        except custom_user.DoesNotExist:
            return render(request, 'user_login.html', {'user404': 'Wrong credentials'})

    return render(request, 'user_login.html')



@never_cache
def user_home(request):
    if 'username' in request.session:
        username = request.session['username']
        users = custom_user.objects.filter(username=username)

        if users.exists():
            user = users.first()

            if not user.is_superuser:
                categories = category.objects.all()
                best_selling_products = Product.objects.order_by('-sales_count')[:4]
                wardrobe_essentials = Product.objects.filter(wardrobe_essential=True)[:4]
                return render(request, 'user_home.html', {
                    'categories': categories,
                    'best_selling_products': best_selling_products,
                    'wardrobe_essentials': wardrobe_essentials
                })
            else:
                return redirect('adminhome')

    return redirect('userlogin')







def user_logout(request):
    if 'username' in request.session:
        request.session.flush()
        return redirect('user_login')
    
def signup(request):
    if 'name' in request.session:
        return render(request, 'user_home.html')
    # if request.user.is_authenticated:
    #  return redirect('adminhome')
    if request.method == 'POST':
        print("haiiiiiiiiii")
        # Retrieve form data
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        phone_number = request.POST.get("phone_number")
        print(phone_number)

        error = None
        if not name or name.strip() == '':
            error = 'Name is required.'
        elif not email or email.strip() == '':
            error = 'Email is required.'
        elif not phone_number or phone_number.strip() == '' or len(phone_number) != 10 or not phone_number.isdigit():
            error = 'Invalid phone number. Please provide a 10-digit number.'
        elif password != cpassword:
            error = 'Passwords do not match.'    

        if error:
            return render(request, 'signup.html', {'error': error})

        if not error:
            # Generate a random 6-digit OTP
            otp = str(random.randint(100000, 999999))

            # Send the SMS using Vonage
            responseData = sms.send_message(
                {
                    "from": "Vonage APIs",
                    "to": "+918156814429",
                    "text": f"Your OTP is: {otp}",
                }
            )
            if responseData["messages"][0]["status"] == "0":
                print("Message sent successfully.")
            else:
                print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

            # Save the OTP and other details in the Uuser model
            form =custom_user(username=name, email=email, password=password,
                         phone_number=phone_number)
            print(form.username)
            form.save()
            request.session['otp'] = otp
            return redirect('otp_grn')
            # return render(request, 'otplogin.html', {'otp': otp})

    else:
        return render(request, 'signup.html')
    


# @never_cache
# def user_home(request):
#     if 'username' in request.session:
#         username = request.session['username']
#         users = custom_user.objects.filter(username=username)

#         if users.exists():
#             user = users.first()

#             if not user.is_superuser:
#                 categories = category.objects.all()
#                 best_selling_products = Product.objects.order_by('-sales_count')[:4]
#                 wardrobe_essentials = Product.objects.filter(wardrobe_essential=True)[:4]
#                 return render(request, 'user_home.html', {
#                     'categories': categories,
#                     'best_selling_products': best_selling_products,
#                     'wardrobe_essentials': wardrobe_essentials
#                 })
#             else:
#                 return redirect('adminhome')

#     return redirect('userlogin')







# @never_cache
# def user_home(request):
#     if 'username' in request.session:
#         username = request.session['username']
#         users = custom_user.objects.filter(username=username)

#         if users.exists():
#             user = users.first()

#             if not user.is_superuser:
#                 categories = category.objects.all()
#                 best_selling_products = Product.objects.order_by('-sales_count')[:4]
#                 wardrobe_essentials = Product.objects.filter(wardrobe_essential=True)[:4]
#                 return render(request, 'user_home.html', {
#                     'categories': categories,
#                     'best_selling_products': best_selling_products,
#                     'wardrobe_essentials': wardrobe_essentials
#                 })
#             else:
#                 return redirect('adminhome')
    
#     # If the user is new and has just signed up, redirect them to the user home page.
#     # This will trigger the code above to load the products and categories for the new user.
#     if 'signup_success' in request.session:
#         return redirect('userhome')

#     return redirect('userlogin')
   
    
def otp_grn(request):
    if request.method == 'POST':
        otp= request.session['otp']
        if request.POST.get('otp') == otp:
            del request.session['otp']
            return render(request, 'user_home.html')
        else:
            # OTP is invalid, render the OTP verification page again with an error message
            msg = 'Enter valid OTP'
            return render(request, 'otplogin.html', {'msg': msg})
        
    else:
        # Render the OTP verification page
        return render(request, 'otplogin.html')  
def otplogin(request):
    return render(request, 'otplogin.html') 






from django.shortcuts import render, get_object_or_404
from .models import Product
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variants = Variant.objects.filter(Product=product)
    sizes = Variant.objects.filter(Product=product).values_list('Size__size', flat=True).distinct()
    colors = Variant.objects.filter(Product=product).values_list('Color__color', flat=True).distinct()
    return render(request, 'product_detail.html', {'product': product, 'sizes': sizes, 'colors': colors,'variants': variants})




# def variant_detail(request, product_id, variant_id):
#     product = get_object_or_404(Product, id=product_id)
#     variants = Variant.objects.filter(Product=product)
#     return render(request, 'variants.html', {'product': product, 'variants': variants})
def variant_detail(request, product_id, variant_id):
    product = get_object_or_404(Product, id=product_id)
    variant = get_object_or_404(Variant, id=variant_id, Product=product)
    return render(request, 'variants.html', {'product': product, 'variant': variant})




def user_product(request, Category_id):
    # products = Product.objects.all()
    # categories = category.objects.all()  # Retrieve all categories for the navigation menu
    categoryobj=category.objects.get(id=Category_id)
    products = Product.objects.filter(category=categoryobj)
    # if category_id:
    #     try:
    #         category = category.objects.get(id=category_id)
    #         products = Product.filter(category=category)
    #     except category.DoesNotExist:
    #         pass  # Handle the case where the category ID is invalid

    context = {
        'products': products,
       
    }

    return render(request, 'user_product.html', context)










    
    # <_____________________________________ADMIN PART____________________________>

@never_cache
def admin_login(request):
    if 'username' in request.session:
        username = request.session['username']
        user = custom_user.objects.get(username = username)

        if user.is_superuser:
            return redirect('adminhome')
        else:
            return redirect('userhome')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = custom_user.objects.get(username = username, password = password)
            
            if user is not None:
                if user.is_superuser:    
                    request.session['username'] = username
                    return redirect('adminhome')
                else:
                    return render(request, 'admin_login.html', {'admin404': 'Please use user login'})
            
        except custom_user.DoesNotExist:
            return render(request, 'admin_login.html', {'admin404': 'Wrong credentials'})

    return render(request, 'admin_login.html')


@never_cache
def admin_home(request):
    
    if 'username' in request.session: 
        username = request.session['username']
        user = custom_user.objects.get(username=username)
    
        if user.is_superuser:
            
            search = request.POST.get('search')

            if search:
                details = custom_user.objects.filter(username__istartswith = search)
            else:
                details = custom_user.objects.filter(is_superuser = False)
            return render(request, 'admin_home.html', {'detailskey':details})
    
    return redirect('user_login')

# 1 USER________________________________________________________________________
def admin_user(request):
    users = custom_user.objects.all()
    return render(request, 'admin_user.html', {'users': users})

def block_unblock_user(request, user_id):
    user = custom_user.objects.get(id=user_id)
    user.status = not user.status  # Toggle the status (block/unblock)
    user.save()
    return redirect('admin_user')

# 2 PRODUCTS_______________________________________________________________
def products(request):
    product = Product.objects.all()
    return render(request,'products.html',{"prdts":product})

from django.shortcuts import render, get_object_or_404
from .models import Product

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'edit_product.html', {'product': product})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Delete the product
        product.delete()

        # Redirect to a success page or show a success message
        # ...

        # For example, you can redirect back to the 'products' page
        return redirect('products')

    return render(request, 'delete_product.html', {'product': product})

# 3category________________________________________________________________

def category_view(request):
    categories = category.objects.all()  # Retrieve all categories
    return render(request, 'category.html', {'categories': categories})





def edit_category(request, category_id):
    # Logic to retrieve the category by ID and process the edit action
    # Replace the following placeholder code with your implementation
    category = category.objects.get(id=category_id)
    if request.method == 'POST':
        # Process the form data and save the changes to the category
        # Redirect to the appropriate page after editing
        return redirect('category')
    return render(request, 'edit_category.html', {'category': category})

def delete_category(request, category_id):
    # Logic to retrieve the category by ID and process the delete action
    # Replace the following placeholder code with your implementation
    category = category.objects.get(id=category_id)
    if request.method == 'POST':
        # Perform the deletion of the category
        # Redirect to the appropriate page after deletion
        return redirect('category')
    return render(request, 'delete_category.html', {'category': category})


