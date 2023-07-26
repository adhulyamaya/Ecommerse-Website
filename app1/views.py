import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import custom_user,Product
from django.contrib.auth.models import User
from decimal import Decimal
 
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from .models import *
from .models import Wishlist
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product ,OrderItems

import random,vonage
from vonage import Sms

from .models import Product
import razorpay
from PINKVILLA.settings import RAZORPAY_API_SECRET_KEY,RAZORPAY_API_KEY


client=vonage.Client(key="23594a08",secret="asBI3u5U6nnRnMd6")
sms=vonage.Sms(client)

from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
import razorpay
from razorpay import Client

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import JsonResponse



from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import letter
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import xlsxwriter
# import io
# from datetime import datetime
# from django.shortcuts import render
# from django.http import FileResponse
# import xlsxwriter
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib import colors
# from .models import Order



@never_cache
def user_login(request):
    if 'username' in request.session:
        return redirect(user_home)
    else:
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
                        return render(request, 'admin_home.html')

            except custom_user.DoesNotExist:
                return render(request, 'user_login.html', {'user404': 'Wrong credentials'})

    return render(request, 'user_login.html')


# USER_HOME AFTER LOGIN


@never_cache

def user_home(request):

    if 'username' in request.session: 

        username = request.session["username"]
        user = custom_user.objects.get(username=username)
        wishlistobj = Wishlist.objects.filter(username=user)
        wishlist_count = wishlistobj.count()
        cart = Cart.objects.filter(username = user)
        cart_count = cart.count()


        categories = category.objects.all()
        best_selling_products = Product.objects.order_by('-sales_count')[:4]
        wardrobe_essentials = Product.objects.filter(wardrobe_essential=True)[:4]    
        return render(request, 'user_home.html', {
            'categories': categories,
            'best_selling_products': best_selling_products,
            'wardrobe_essentials': wardrobe_essentials,
            'wishlist_count':wishlist_count,
            "cart":cart,
            "cart_count":cart_count
                   
        })
    else:
        return redirect('home_before')


# USER_HOME BEFORE LOGIN

def home_before(request):
    
    categories = category.objects.all()
    best_selling_products = Product.objects.order_by('-sales_count')[:4]
    wardrobe_essentials = Product.objects.filter(wardrobe_essential=True)[:4]
    return render(request, 'home_before.html', {'categories': categories, 'best_selling_products': best_selling_products,
    'wardrobe_essentials': wardrobe_essentials})



def user_logout(request):
    if 'username' in request.session:
        request.session.flush()
        return redirect('home_before')
    
def signup(request):
    if 'name' in request.session:
        return render(request, 'user_home.html')

    if request.method == 'POST':
        
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



def shop(request):
    username = request.session["username"]
    user = custom_user.objects.get(username=username)
    wishlistobj = Wishlist.objects.filter(username=user)
    wishlist_count = wishlistobj.count()

    products = Product.objects.all()
    brands = Brand.objects.all()
    
    selected_brands = request.POST.getlist('brands') 
    if selected_brands:
        # Filter the products based on the selected brands
        products = products.filter(brand__id__in=selected_brands)


    # Add pagination to the products queryset
    paginator = Paginator(products, 12)  # Show 12 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, deliver the first page.
        products = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page of results.
        products = paginator.page(paginator.num_pages)    
    
    context = {
        "products": products,
        "brand": brands,
        "wishlist_count":wishlist_count
    }
    return render(request,'shop.html',context)



def shop_before(request):
    products = Product.objects.all()
        
    context = {
            "products":products,
            
        }   
    return render (request,"shop_before.html",context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    colobj = Color.objects.all()
    sizeobj = Size.objects.all()
    variants = Variant.objects.filter(Product=product)
    sizes = Variant.objects.filter(Product=product).values_list('Size__size', flat=True).distinct()
    colors = Variant.objects.filter(Product=product).values_list('Color__color', flat=True).distinct()

    # Handle form submission
    if request.method == 'POST':
        selected_colors = request.POST.getlist('color')
        selected_size = request.POST.get('size')

        if selected_colors:
            variants = variants.filter(Color__id__in=selected_colors)

        if selected_size:
            variants = variants.filter(Size__id=selected_size)

    context = {
        'product': product,
        'sizes': sizes,
        'colors': colors,
        'variants': variants,
        'colobj': colobj,
        'sizeobj': sizeobj,
    }
    return render(request, 'product_detail.html', context)



def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    colobj = Color.objects.all()
    sizeobj = Size.objects.all()
    variants = Variant.objects.filter(Product=product)
    sizes = Variant.objects.filter(Product=product).values_list('Size__size', flat=True).distinct()
    colors = Variant.objects.filter(Product=product).values_list('Color__color', flat=True).distinct()
    selected_color = request.POST.getlist('colors')

    selected_color = request.POST.getlist('colors')
    if selected_color:
        variants = variants.filter(Color__id__in=selected_color)
    
    selected_size = request.POST.get('size')
    if selected_size:
        variants = variants.filter(Size__id__in = selected_size)   
    context = {'product': product, 'sizes': sizes, 'colors': colors,'variants': variants,"colobj":colobj,"sizeobj":sizeobj}
    return render(request, 'product_detail.html',context)


def variant_detail(request, product_id, variant_id):
    product = get_object_or_404(Product, id=product_id)
    variant = get_object_or_404(Variant, id=variant_id, Product=product)
    return render(request, 'variants.html', {'product': product, 'variant': variant})


def user_profile(request):
    username = custom_user.objects.get(username=request.session["username"])
    user_phone = username.phone_number
    addresses = Address.objects.filter(username=username)
    wishlistobj = Wishlist.objects.filter(username = username)
    wishlist_count = Wishlist.objects.filter(username = username).count() 
    cart = Cart.objects.filter(username = username)
    cart_count = Cart.objects.filter(username = username).count()

    context = {
        'username': username,
        'phone_number': user_phone,
        'addresses': addresses,
        'wishlistobj':wishlistobj,
        'wishlist_count':wishlist_count,
        'cart':cart,
        'cart_count': cart_count
    }

    return render(request, "user_profile.html", context)

def user_address(request):
    if "username" in request.session:
        if request.method == 'POST':
            # user_id = request.POST.get("user_id")
            # username = custom_user.objects.filter(id=user_id).first()
            username = request.session["username"]
            userobj = custom_user.objects.get(username=username)
            print(username,"???????????????hi",userobj)
            flat = request.POST.get("flat")
            locality = request.POST.get("locality")
            city = request.POST.get("city")
            pincode = request.POST.get("pincode")
            state = request.POST.get("state")
        
            
            address = Address(username=userobj,flat=flat,locality=locality, city=city,pincode=pincode, state=state,
            )
            address.save()
            print("Address saved:>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", address) 
            return redirect('user_profile')





def user_proeditadd(request,address_id):    
    
    if request.method == 'POST':
        flat = request.POST.get("flat")
        locality = request.POST.get("locality")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        state = request.POST.get("state")

        addressobj = Address.objects.get(id=address_id)
        print(addressobj,">>>>>>error")
        addressobj.flat = flat
        addressobj.locality = locality
        addressobj.city = city
        addressobj.pincode = pincode
        addressobj.state = state
        
        addressobj.save()
        return redirect(user_profile)
    
    return render(request, 'user_proeditadd.html', {'address': addressobj})








def add_to_cart(request):
    username=custom_user.objects.get(username=request.session["username"])
    variant_id = request.POST.get("variant_id")
    variant = Variant.objects.get(id=variant_id)
    try:
        cart_item = Cart.objects.get(username=username, variant=variant)
        # If the variant exists, increment the quantity
        cart_item.quantity += 1
        cart_item.save()
    except Cart.DoesNotExist:
        # If the variant does not exist, create a new cart item
        cart_item = Cart(username=username, variant=variant, quantity=1)
        cart_item.save()

        print(cart_item,"achuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
    # cart = Cart(username=username, variant=variant,quantity = 1)
    # cart.save()
    return redirect("show-cart")




# def show_cart(request):
#   username=custom_user.objects.get(username=request.session["username"])
#   cart = Cart.objects.filter(username = username)
#   cart_count = Cart.objects.filter(username = username).count()
#   amount = 0
#   quantityobj=0
#   for i in cart:
#       value = i.quantity * i.variant.price
#       amount = amount + value
#       total = amount +40
#       quantityobj +=i.quantity
#   return render (request,'addtocart.html',{'cart': cart,'total':total,'amount':amount,
#                                            'quantityobj':quantityobj,"cart_count":cart_count})



from django.contrib import messages
from django.http import HttpResponseRedirect



def show_cart(request):
    username = custom_user.objects.get(username=request.session["username"])
    cart_items = Cart.objects.filter(username=username)
    cart_count = cart_items.count()
    couponobj = None
    if request.method == 'POST':
        coupon = request.POST.get("coupon")
        couponobj = Coupon.objects.filter(coupon_code__icontains=coupon)

        if not couponobj.exists():
            messages.warning(request, 'Invalid Coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        for cart_item in cart_items:
            if cart_item.coupon:
                messages.warning(request, 'Coupon already applied')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            cart_item.coupon = couponobj[0]
            cart_item.save()
            messages.success(request, 'Coupon applied successfully!')

    amount = 0
    quantityobj = 0
    for cart_item in cart_items:
        value = cart_item.quantity * cart_item.variant.price
        amount += value
        quantityobj += cart_item.quantity

    coupon_discount = 0
    if couponobj and couponobj.exists(): 
        print(couponobj,",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
        coupon_discount = couponobj[0].discount_price
        print(coupon_discount,"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        amount =Decimal(amount) - coupon_discount
        print (amount)

    total = amount + 40
    print(total,">>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    context = {'cart': cart_items,
        'total': total,
        'amount': amount,
        'quantityobj': quantityobj,
        'coupon_discount': coupon_discount,
        'cart_count': cart_count }

    return render(request, 'addtocart.html',context)



def cart_inc(request,item_id):
    cartobj = Cart.objects.get(id=item_id)
    username = cartobj.username
    variant = cartobj.variant
    cart_item = Cart.objects.filter(username = username , variant = variant).first()
    if cart_item :
        cart_item.quantity+=1
        cart_item.save()
    return redirect("show-cart")

def cart_dec(request,item_id):
    cartobj = Cart.objects.get(id=item_id)
    username = cartobj.username
    variant = cartobj.variant
    cart_item = Cart.objects.filter(username = username , variant = variant).first()
    if cart_item :
        cart_item.quantity-=1
        cart_item.save()
    return redirect("show-cart")


def cart_remove(request,item_id):
    cartobj = Cart.objects.get(id = item_id)
    cartobj.delete()
    return redirect ("show-cart")



def checkout(request):
  if "username" in request.session:
    print(RAZORPAY_API_SECRET_KEY,"####################")
    username=custom_user.objects.get(username=request.session["username"])
    cartobj = Cart.objects.filter(username = username)
    addobj = Address.objects.filter(username = username)
    if request.method == "POST":
        username = request.session.get("username")
        customer = custom_user.objects.get(username=username)
        cartobj = Cart.objects.filter(username = customer)
        addobj = Address.objects.filter(username = customer)
        if request.method == "POST":
            username = request.session.get("username")
            customer = custom_user.objects.get(username=username)
            cartobj = Cart.objects.filter(username = customer)
            addobj = Address.objects.filter(username = customer)

            addressid = request.POST.get("address")
            address = Address.objects.get(id=addressid)
            date_ordered = datetime.date.today()
            
            orderobj = Order(customer = customer, address=address, date_ordered=date_ordered, total = 0)
            orderobj.save()
        
            for item in cartobj:
                pdtvariant = item.variant
                price = item.variant.price
                quantity = item.quantity
                item_total = quantity*price

                orderitemobj = OrderItems(variant = pdtvariant, order = orderobj,
                                            quantity=quantity, price=price, total = item_total)
                    
                orderitemobj.save()
                print(orderitemobj,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

                pdtvariant.quantity -= quantity
                pdtvariant.save()

                orderobj.total += item_total

                item.delete()
            orderobj.save()
            print("Order successfully processed!")
            return redirect(ordersuccess) 
             
    total_cost = sum(item.total_cost() for item in cartobj)+40

    coupon_discount = sum(item.coupon.discount_price for item in cartobj if item.coupon)

    total_cost =Decimal(total_cost) - coupon_discount

    client = razorpay.Client(
    auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
    amount=int(total_cost*100)
    currency='INR'
    data = dict(amount=amount,currency=currency,payment_capture=1)            
    payment_order = client.order.create(data=data)
    payment_order_id=payment_order['id']  
    context = {
            'username': username,
            'cartobj': cartobj,
            'addobj': addobj,
            'total_cost':total_cost,
            "api_key":RAZORPAY_API_KEY,
            "amount":400,
            "order_id":payment_order_id,
            }
    return render (request,"checkout.html",context)
  

def ordersuccess(request):
    return render (request,"ordersuccess.html")

def user_product(request, Category_id):
    categoryobj=category.objects.get(id=Category_id)
    products = Product.objects.filter(category=categoryobj)
    context = {
        'products': products,
       
    }
    return render(request, 'user_product.html', context)

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def add_to_wishlist(request):
    username=custom_user.objects.get(username=request.session["username"])
    variant_id = request.POST.get("variant_id")
    variant = Variant.objects.get(id=variant_id)
    if not Wishlist.objects.filter(username=username, variant=variant).exists():
            wishlist_item = Wishlist(username=username, variant=variant)
            wishlist_item.save()
            messages.success(request, "Product added to wishlist successfully.")
    else:
        messages.info(request, "Product is already in your wishlist.")
    return redirect("wishlist")


def wishlist(request):
    username=custom_user.objects.get(username=request.session["username"])
    wishlistobj = Wishlist.objects.filter(username = username)   
    return render (request,"wishlist.html",{'wishlistobj': wishlistobj})


def wishlist_remove(request,item_id):
    wishlistobj = Wishlist.objects.get(id = item_id)
    wishlistobj.delete()
    return redirect ("wishlist")


def search_products(request):
    query = request.GET.get('q')  
    results = []
    if query:
        results = Product.objects.filter(name__icontains=query)

    return render(request, 'search_results.html', {'results': results, 'query': query})  

def changepassword(request):
    if "username" in request.session:
        userobj=custom_user.objects.get(username=request.session["username"])
        if request.method == "POST":
            old_password = request.POST.get('old_password')
            if userobj.password!=old_password:
                return render(request, 'changepassword.html', {'error_message': 'Old Password is not correct'})
            
            new_pass1 = request.POST.get("new_password1")
            print(new_pass1)
            new_pass2 = request.POST.get("new_password2")
            print(new_pass2)

            if new_pass1 != new_pass2:
                return render(request, 'changepassword.html', {'error_message': 'New passwords do not match'})
            userobj.password=new_pass1
            userobj.save()
            return redirect(user_profile)
        return render(request, 'changepassword.html')


def cancel_order(request, order_id):
        order = Order.objects.get(id=order_id)

        order.delete()
        order.order_status = 'cancelled'
        order.save()
        return redirect('view_orders') 

def view_order(request):
    orderobj = Order.objects.all()
    context = {
        "orderobj":orderobj
    }
    return render(request, 'view_order.html',context )




def userorder_items(request, order_id):
    orderobj = Order.objects.get(id=order_id)
    items = OrderItems.objects.filter(order=orderobj)
    context = {
        "itemobj": items,
       
    }
    return render(request, 'userorder_items.html', context) 

def order_history(request):
    return render(request, 'order_history.html' ) 
import datetime
from django.shortcuts import redirect

def razorupdateorder(request):
     
    username = request.session.get("username")
    customer = custom_user.objects.get(username=username)
    cartobj = Cart.objects.filter(username = customer)

    addressval=request.GET.get("addressval")
    print(addressval,"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
    finalprice =request.GET.get("finalprice")
    
    address = Address.objects.get(username = customer,flat = addressval)
    date_ordered = datetime.date.today()
    
    orderobj = Order(customer = customer, address=address, date_ordered=date_ordered, total = finalprice,payment_type="razor pay")
    orderobj.save()
    for item in cartobj:

        pdtvariant = item.variant
        price = item.variant.price
        quantity = item.quantity
        item_total = quantity*price

        orderitemobj = OrderItems(variant = pdtvariant, order = orderobj,
                                    quantity=quantity, price=price, total = item_total)
            
        orderitemobj.save()
        print(orderitemobj,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        pdtvariant.quantity -= quantity
        pdtvariant.save()
        item.delete()

    return JsonResponse({"message": "Done"})


from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_invoice(request, order_id):
    # Fetch the order details from the database using the order_id
    order = Order.objects.get(id=order_id)
    order_items = OrderItems.objects.filter(order=order)

    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')

    # Set the Content-Disposition header to force download
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'

    # Create a PDF canvas using reportlab
    p = canvas.Canvas(response, pagesize=letter)

    # Write the invoice details to the PDF
    p.drawString(100, 800, f'Invoice for Order #{order_id}')
    p.drawString(100, 780, f'Customer: {order.customer.username}')
    p.drawString(100, 760, 'Order Items:')
    
    y = 740
    for item in order_items:
        p.drawString(120, y, f'{item.variant.product.name} x {item.quantity} - ${item.total}')
        y -= 20

    # Calculate the total amount for the order
    total_amount = sum(item.total for item in order_items)
    p.drawString(100, y, f'Total Amount: ${total_amount}')

    # Save the PDF content
    p.showPage()
    p.save()

    return response



# views.py
from io import BytesIO 
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def download_invoice(request, order_id):
    # Retrieve the order and other relevant data based on the order_id
    # (You may need to adjust this part based on your data model)
    try:
        from app1.models import Order
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse("Order not found.", status=404)

    # Generate the PDF content using reportlab
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Customize the content of the invoice based on your requirements
    pdf.drawString(100, 800, f"Invoice for Order #{order_id}")
    pdf.drawString(100, 780, f"Customer: {order.customer.username}")
    pdf.drawString(100, 760, f"Address: {order.address}")
    pdf.drawString(100, 740, f"Total Amount: {order.total}")
    # Add more relevant information as needed

    pdf.save()

    # Set the buffer position to the start to ensure the entire content is written to the response
    buffer.seek(0)

    # Create a response with PDF content
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_order_{order_id}.pdf"'
    return response



# <_____________________________________ADMIN PART____________________________>

@never_cache
def admin_login(request):
    if 'username' in request.session:
        return redirect(admin_home)
    else:
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

def admin_logout(request):
    if 'username' in request.session:
        request.session.flush()
        return redirect('adminlogin')

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
    product = Product.objects.get(id=product_id)
    categoryobjs = category.objects.all()
    brandobjs = Brand.objects.all()
    existing_image = product.image if product.image else None
    if request.method == "POST":
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        cat = request.POST.get('category')
        image = request.FILES.get('image')
        description = request.POST.get('description')

        catobj = category.objects.filter(name=cat).first()
        
        brandobj = Brand.objects.get(brand=brand)
        
        print(catobj,">>>>>>>",name,brandobj)
        product.name=name
        product.brand=brandobj
        product.category=catobj
        product.description=description
        if image:
            product.image=image
        else:
            product.image=existing_image
        product.save()
        return redirect(products)

    return render(request, 'edit_product.html', {'product': product,'categoryobjs':categoryobjs,'brandobjs':brandobjs})





def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':       
        product.delete()
        return redirect('products')
    return render(request, 'delete_product.html', {'product': product})


def category_view(request):
    categories = category.objects.all()
    return render(request, 'category.html', {'categories': categories})

def user_proeditadd(request,address_id):    
    address = Address.objects.get(id=address_id)
    if request.method == 'POST':
        flat = request.POST.get("flat")
        locality = request.POST.get("locality")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        state = request.POST.get("state")
        print(flat,">>>>>>>>")
        address.flat = flat
        address.locality = locality
        address.city = city
        address.pincode = pincode
        address.state = state
        address.save()
        return redirect(user_profile)   
    return render(request, 'user_proeditadd.html', {'address': address, })

def add_category(request):
    return render(request, 'add_category.html')

    
      
def add_product(request):
    brands=Brand.objects.all()
    catobj=category.objects.all()
    context={
        "brands":brands,
        "category":catobj
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        brandobj=Brand.objects.get(brand=brand)
        category_name = request.POST.get('category')
        catobj=category.objects.get(name=category_name)
        description = request.POST.get('description')
        image = request.FILES.get('image')
        print(image,"...........................................................")
        new_product = Product(name=name, brand=brandobj, category=catobj, description=description, image=image)
        new_product.save()
        return redirect(products)
    return render(request, 'add_product.html',context)


def edit_category(request, category_id):
    category_obj = category.objects.get(id=category_id)
    print(category_obj,"?????????????")
    if request.method == 'POST':  
        name = request.POST.get("category_name") 
        category_obj.name = name
        print(name,">>>>>>>>")
        new_category = category(id=category_id, name=name)       
        new_category.save()
        return redirect('category')
    return render(request, 'edit_category.html', {'category': category_obj})


def delete_category(request, category_id):
    categoryobj = category.objects.get(id=category_id)
    if request.method == 'POST':       
        return redirect('category')
    return render(request, 'delete_category.html', {'category': categoryobj})


def edit_order(request,order_id):
    orderobj=Order.objects.all()
    order_obj = Order.objects.get(id= order_id)
    order_status_choices = Order.ORDER_STATUS_CHOICES
    if request.method == 'POST':  
        name = request.POST.get("order_status") 
        order_obj.order_status = name        
        order_obj.save()
        return redirect('orderadmin')    
    return render(request, 'edit_order.html',{'orderobj':orderobj ,"order_status_choices":order_status_choices })


def orderadmin(request,):
    orderobj = Order.objects.all()
    context = {
        "orderobj":orderobj
    }
    return render (request,"orderadmin.html",context)


def order_items(request, order_id):
    orderobj = Order.objects.get(id=order_id)
    items = OrderItems.objects.filter(order=orderobj)  
    context = {
        "itemobj": items,   
    }
    return render(request, 'order_items.html', context)


def userorder_items(request, order_id):
    orderobj = Order.objects.get(id=order_id)
    items = OrderItems.objects.filter(order=orderobj)  
    context = {
        "itemobj": items,   
    } 
    return render(request, 'userorder_items.html', context)


def admin_variant(request):
    variantobj = Variant.objects.all()
    return render(request, 'admin_variant.html',{ "variantobj":variantobj })


def color_admin(request):
    color = Color.objects.all()
    context ={
        "color":color
    }
    return render(request, 'color_admin.html',context)


def size_admin(request):
    size = Size.objects.all()
    context ={
        "size":size
    }
    return render (request,'size_admin.html',context)

def admin_coupon(request):
    couponobj = Coupon.objects.all()
    context = {
        "couponobj":couponobj
    }
    return render (request,'admincoupon.html',context)




# def salesreport(request):
#     return render (request,'salesreport.html')


def salesreport(request):
    if request.method=="POST":
        if "show" in request.POST:
            start_date=request.POST.get("start_date")
            end_date=request.POST.get("end_date")
            orderobjs = Order.objects.filter(date_ordered__range=[start_date, end_date])
            if orderobjs.count()==0:
                message="Sorry! No orders in this particular date range"
                context={"orderobjs":orderobjs,"message":message}
            else:

                context={"orderobjs":orderobjs}
            return render(request,"salesreport.html",context)
        elif "download" in request.POST:
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=letter)
            elements = []

            # Add heading
            styles = getSampleStyleSheet()
            heading_style = styles['Heading1']
            heading = "Sales Report"
            heading_paragraph = Paragraph(heading, heading_style)
            elements.append(heading_paragraph)
            elements.append(Spacer(1, 12))  # Add space after heading

            ords = Order.objects.filter(orderdate__range=[start_date, end_date])
            

            if ords:
                data = [['Sl.No.', 'Name', 'Product', 'House', 'Order Date', 'Order Status', 'Quantity']]
                slno = 0
                for ord in ords:
                    slno += 1
                    row = [slno, ord.user.name, ord.product.name, ord.address.house, ord.orderdate, ord.orderstatus, ord.quantity]
                    data.append(row)

                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))

                elements.append(table)
            else:
                elements.append(Paragraph("No orders", styles['Normal']))
            if elements:

                doc.build(elements)
                buf.seek(0)
                return FileResponse(buf, as_attachment=True, filename='Orders.pdf')
        
        elif "downloadinexcel" in request.POST:

            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")



            ords = Order.objects.filter(orderdate__range=[start_date, end_date])

            # Create Excel workbook and worksheet
            workbook = xlsxwriter.Workbook("Sales_Report.xlsx")
            worksheet = workbook.add_worksheet('Sales Report')

            # Write the table headers
            headers = ['Sl.No.', 'Name', 'Product', 'House', 'Order Date', 'Order Status', 'Quantity']
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)

            # Write the data rows
            row = 1
            for slno, ord in enumerate(ords, start=1):
                worksheet.write(row, 0, slno)
                worksheet.write(row, 1, ord.user.name)
                worksheet.write(row, 2, ord.product.name)
                worksheet.write(row, 3, ord.address.house)
                worksheet.write(row, 4, str(ord.orderdate))
                worksheet.write(row, 5, ord.orderstatus)
                worksheet.write(row, 6, ord.quantity)
                row += 1

            workbook.close()

            # Create a file-like buffer to receive the workbook data
            buf = io.BytesIO()
            
            buf.seek(0)
            

            # Return the Excel file as a FileResponse
            return FileResponse(buf, as_attachment=True, filename='Sales_Report.xlsx', content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    return render (request,'salesreport.html')