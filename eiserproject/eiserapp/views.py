from itertools import count
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.utils.timezone import now
from django.utils.decorators import method_decorator
from django.views import View
from django.views import View
from django.core.mail import send_mail
import random
import requests
import hashlib
import string
from datetime import datetime, timedelta
from django.db.models import Avg
from django.db.models import Sum
from decimal import Decimal
from django.db.models import Count
from django.db.models import Prefetch,Q
from collections import defaultdict
from .models import *

# Create your views here.
def login(request):
    return render(request,"login.html")

def login_post(request):
    emailorphone = request.POST['emailorphone']
    password = request.POST['password']
    user=Login.objects.filter(emailorphone=emailorphone).first()
    if user:
        salt = Login.objects.get(emailorphone=emailorphone).salt
        print(salt)
        password = salt+password
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        log=Login.objects.filter(emailorphone=emailorphone,password=password).first()
        if log:
            request.session['lid']=log.id
            if log.type == "Seller":
                return redirect('/seller_dashboard/')
            elif log.type == "DeliveryBoy":
                return redirect('/deliveryboy_home/')
            else: #for customers
                return redirect('/index/')
        else:
            return HttpResponse('''<script>alert("Invalid credentials. Please try again.");window.location="/login/"</script>''')
    else:
        return HttpResponse('''<script>alert("Invalid credentials. Please try again.");window.location="/login/"</script>''')

#CUSTOMER:

def signup(request):
    log=Login.objects.all()
    return render(request,"signup.html", {'login':log})

def signup_post(request):
    name = request.POST['name']
    emailorphone = request.POST['emailorphone']
    password = request.POST['password']
    salt=''.join(random.choices(string.ascii_letters,k=7))
    # print(str(salt))
    password=salt+password
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    photo = request.FILES.get('photo',None) # Set photo to None if not uploaded
    place = request.POST['place']
    pincode = request.POST['pincode']
    state = request.POST['state']
    gender = request.POST['gender']
    if Signup.objects.filter(emailorphone=emailorphone).exists():
        return HttpResponse('''<script>alert("An account with the provided email or phone number already exists.");window.location="/signup/"</script>''')
    
    lg=Login(
        emailorphone=emailorphone,
        password=password,
        salt=salt,
        type='Customer'
    )
    lg.save()
    sg=Signup(
        name=name,
        emailorphone=emailorphone,
        photo=photo,
        place=place,
        pincode=pincode,
        state=state,
        gender=gender,
        login_id=lg.id
    )
    sg.save()
    return HttpResponse('''<script>alert("Registered successfully! Please login to continue.");window.location="/login/"</script>''')

def send_sms(message, email_or_phone):
    url = "http://192.168.29.149:8080/message"
    auth = ("sms", "F0H5UDNV")
    payload = {
        'message': message,
        'phoneNumbers' : [email_or_phone]
    }
    response = requests.post(url, json=payload, auth=auth)
    return response.status_code

def forgot_password(request):
    return render(request, "forgot_password.html")

def forgot_password_post(request):
    if request.method == 'POST':
        email_or_phone = request.POST['emailorphone']
        log = Login.objects.filter(emailorphone=email_or_phone).first()
        if log:
            logd = Login.objects.get(emailorphone=email_or_phone).id
            kk = Login.objects.get(id=logd).emailorphone
            request.session['email_or_phone'] = kk

            # Generate OTP
            otp = f"{random.randint(100000, 999999)}"
            log.otp = otp
            log.otp_expiry = now() + timedelta(minutes=5)  # OTP expires in 5 minutes
            log.otp_cooldown = now() + timedelta(minutes=1)  # Resend cooldown of 1 minute
            log.save()

            # Send OTP to email or phone
            if '@' in email_or_phone:
                send_mail(
                    'Eiser account password reset OTP',
                    f'Your OTP is {otp}. It is valid for 5 minutes. Do not share.',
                    'muhammedshabeebkt2016@gmail.com',
                    [email_or_phone],
                    fail_silently=False,
                )
            else:
                send_sms(f'Your Eiser account recovery OTP is {otp}. It is valid for 5 minutes.', email_or_phone)

            return redirect('/verify_otp')
        else:
            return HttpResponse('''<script>alert("Account associated with the provided email or phone not found.");window.location="/forgot_password/"</script>''')

def resend_otp(request):
    if request.method == 'POST':
        email_or_phone = request.session.get('email_or_phone')
        print(f"Retrieved email_or_phone from session: {email_or_phone}")  # Debugging
        if not email_or_phone:
            return JsonResponse({'status': 'error', 'message': 'Session expired or invalid.'}, status=400)

        log = Login.objects.filter(emailorphone=email_or_phone).first()
        if log and now() > log.otp_cooldown:
            # Generate new OTP
            otp = f"{random.randint(100000, 999999)}"
            log.otp = otp
            log.otp_expiry = now() + timedelta(minutes=5)  # OTP expires in 5 minutes
            log.otp_cooldown = now() + timedelta(minutes=1)  # Resend cooldown of 1 minute
            log.save()

            # Send new OTP
            if '@' in email_or_phone:
                print(f"Sending OTP to email: {email_or_phone}")  # Debugging
                send_mail(
                    'Eiser account password reset OTP',
                    f'Your new OTP is {otp}. It is valid for 5 minutes. Do not share.',
                    'muhammedshabeebkt2016@gmail.com',
                    [email_or_phone],
                    fail_silently=False,
                )
            else:
                print(f"Sending OTP to phone: {email_or_phone}")  # Debugging
                send_sms(f'Your new Eiser account recovery OTP is {otp}. It is valid for 5 minutes.', email_or_phone)

            return JsonResponse({'status': 'success', 'message': 'OTP resent successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Please wait before resending OTP.'}, status=400)


def verify_otp(request):
    email_or_phone = request.session['email_or_phone']
    return render(request,"verify_otp.html", {'email_or_phone': email_or_phone})

def verify_otp_post(request):
    if request.method == 'POST':
        email_or_phone = request.session['email_or_phone']
        entered_otp = request.POST['otp']

        log = Login.objects.filter(emailorphone=email_or_phone, otp=entered_otp).first()
        if log and log.otp_expiry > now():
            log.otp = None  # Clear OTP
            log.otp_expiry = None
            log.save()
            return HttpResponse('''<script>alert("OTP Verification successful! Please reset your password.");window.location="/reset_password/"</script>''')
        else:
            return HttpResponse('''<script>alert("Invalid or expired OTP. Please try again.");window.location="/verify_otp/"</script>''')
        
def reset_password(request):
    # log=Login.objects.filter(id=id).first()
    return render(request,"reset_password.html")

def reset_password_post(request):
    email_or_phone=request.session['email_or_phone']
    new_password=request.POST['password']

    log=Login.objects.get(emailorphone=email_or_phone)

    if log:
        salt = log.salt
        new_password = salt + new_password
        new_password = hashlib.md5(new_password.encode('utf-8')).hexdigest()

        log.password=new_password
        log.save()

        # Clear the session after password reset
        # del request.session['lid']

        return HttpResponse('''<script>alert("Password reset successful. Please log in.");window.location="/login/"</script>''')
    else:
        return HttpResponse ('''<script>alert("An error occurred. Please try again.");window.location="/reset_password/"</script>''')


def index(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    try:
        user = Signup.objects.get(login=request.session['lid'])
    except (Signup.DoesNotExist, KeyError):
        user = None
    products = Product.objects.all()
    wishlist_items = Wishlist.objects.filter(user=user)
    offers = Offer.objects.all()
    cart_items = Cart.objects.filter(user=user,status='Pending')

    # Save the search query if the user is authenticated    
    search_history = []
    if user:
        search_history = SearchHistory.objects.filter(user=user).order_by('-searched_at')[:10]
    

    # Prepare the wishlist with discounted prices
    wishlist_data = []
    # Add discounted prices to each product
    for item in wishlist_items:
        product = item.product
        offer = offers.filter(product_id=product.id).first()  # Get the offer for the product
        if offer:
            discounted_price = round(product.price - (product.price * offer.discount / 100))
        else:
            discounted_price = product.price  # No discount applied

        # Append product data along with discounted price to the list
        wishlist_data.append({
            'id': item.id,
            'product': product,
            'discounted_price': discounted_price,
        })

    # Initialize offer_amount to avoid UnboundLocalError
    offer_amount = 0  # Default value when no cart items exist
    total_price = 0  # Ensure total_price is also defined

    #price calculation:
    if cart_items.exists():
        for item in cart_items:
            # Check for active offer:
            offer = Offer.objects.filter(
                product=item.product,
                sdate__lte=datetime.now(),
                edate__gte=datetime.now()
            ).first()

            if offer:
                offer_amount = round(item.product.price * (1 - offer.discount / 100), 2)
            else:
                offer_amount = item.product.price

            # Check for applied coupon:
            if item.coupon_amount:
                final_price = round(item.coupon_amount * item.quantity, 2)
            else:
                final_price = round(offer_amount * item.quantity, 2)

            # Update the final amount
            item.final_amount = final_price

        total_price = sum(item.final_amount for item in cart_items)
    return render(request,"index.html",{'search_history':search_history,'wishlist': wishlist_data, "cart": cart_items, "discount_price": offer_amount,'categories': categories, 'subcategories': subcategories})

def profile(request):
    user=Signup.objects.get(login=request.session['lid'])
    search_history = []
    if user:
        search_history = SearchHistory.objects.filter(user=user).order_by('-searched_at')[:10]
    return render(request,"profile.html",{'profile':user, 'search_history':search_history})

def profile_edit(request):
    sg=Signup.objects.get(id=id)
    sg.name=request.POST['name']
    if 'photo' in request.FILES:
        sg.photo=request.POST['photo']
    sg.place=request.POST['place']
    sg.pincode=request.POST['pincode']
    sg.state=request.POST['state']
    sg.gender=request.POST['gender']
    sg.save()
    return HttpResponse('''<script>alert("Profile Updated successfully.");window.location="/profile/"</script>''')

def change_password_post(request):
    current_password = request.POST['current_password']
    salt=Login.objects.get(id=request.session['lid']).salt
    current_password=salt+current_password
    current_password = hashlib.md5(current_password.encode('utf-8')).hexdigest()

    log=Login.objects.get(id=request.session['lid'])
    # logpass=Login.objects.get(id=request.session['lid']).password
    logpass=log.password

    if logpass==current_password:
        new_password=request.POST['password']

        # Ensure the new password is not the same as the current password
        new_salt=''.join(random.choices(string.ascii_letters,k=7))
        new_password=new_salt+new_password
        new_password = hashlib.md5(new_password.encode('utf-8')).hexdigest()
        if new_password == logpass:
            return HttpResponse('''<script>alert("New password cannot be the same as the current password! Please try again.");window.location="/profile/"</script>''')
        
        # Update password and salt
        log.salt=new_salt  
        log.password=new_password
        log.save()
        
        return HttpResponse('''<script>alert("Password changed successfully.");window.location="/profile/"</script>''')
    else:
        return HttpResponse('''<script>alert("Current password incorrect! Please try again.");window.location="/profile/"</script>''')
         


#SELLER:

def seller_reg(request):
    log=Login.objects.all()
    return render(request,"seller_reg.html",{'login':log})

def seller_reg_post(request):
    name = request.POST['name']
    emailorphone = request.POST['emailorphone']
    password = request.POST['password']
    salt=''.join(random.choices(string.ascii_letters,k=7))
    # print(str(salt))
    password=salt+password
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    photo = request.FILES.get('photo',None) # Set photo to None if not uploaded
    place = request.POST['place']
    pincode = request.POST['pincode']
    state = request.POST['state']
    gender = request.POST['gender']
    license = request.FILES['license']
    id_proof = request.FILES['id_proof']
    if Seller.objects.filter(emailorphone=emailorphone).exists():
        return HttpResponse('''<script>alert("A seller account with the provided email or phone number already exists.");window.location="/seller_reg/"</script>''')
    
    lg=Login(
        emailorphone=emailorphone,
        password=password,
        salt=salt,
        type='Seller'
    )
    lg.save()
    slr=Seller(
        name=name,
        emailorphone=emailorphone,
        photo=photo,
        place=place,
        pincode=pincode,
        state=state,
        gender=gender,
        license=license,
        id_proof=id_proof,
        login_id=lg.id
    )
    slr.save()
    return HttpResponse('''<script>alert("Seller Registered successfully! Please login to continue.");window.location="/login/"</script>''')

from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Seller, OrderItem, Product

def seller_dashboard(request):
    seller = Seller.objects.get(login=request.session['lid'])
    
    # Fetch relevant data for the dashboard
    total_sales = OrderItem.objects.filter(product__seller=seller).aggregate(total_sales=Sum('price'))['total_sales'] or 0
    completed_orders = OrderItem.objects.filter(product__seller=seller, checkout__payment_status='Completed').count()
    pending_orders = OrderItem.objects.filter(product__seller=seller, checkout__payment_status='Pending').count()
    low_stock_products = Product.objects.filter(seller=seller, instock__lt=10).count()
    
    recent_orders = OrderItem.objects.filter(product__seller=seller).select_related('checkout').order_by('-checkout__date')[:10]
    
    # Fetch monthly sales data for the chart
    monthly_sales = (
        OrderItem.objects
        .filter(product__seller=seller)
        .annotate(month=TruncMonth('checkout__date'))  # Group by month
        .values('month')  # Get the month
        .annotate(total_sales=Sum('price'))  # Calculate total sales for each month
        .order_by('month')  # Order by month
    )
    
    # Prepare data for the chart
    sales_labels = [entry['month'].strftime("%b %Y") for entry in monthly_sales]  # Format: "Jan 2025"
    sales_data = [float(entry['total_sales']) for entry in monthly_sales]  # Convert to float for Chart.js
    
    context = {
        'seller': seller,
        'total_sales': total_sales,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
        'sales_labels': sales_labels,
        'sales_data': sales_data,
    }
    
    return render(request, "seller-dashboard.html", context)

def seller_profile(request):
    seller=Seller.objects.get(login=request.session['lid'])
    return render(request,"seller_profile.html",{'profile':seller})

def seller_profile_edit(request,id):
    slr=Seller.objects.get(id=id)
    slr.name=request.POST['name']
    if 'photo' in request.FILES:
        slr.photo=request.POST['photo']
    slr.place=request.POST['place']
    slr.pincode=request.POST['pincode']
    slr.state=request.POST['state']
    slr.gender=request.POST['gender']
    slr.save()
    return HttpResponse('''<script>alert("Profile Updated successfully.");window.location="/seller_profile/"</script>''')

def seller_change_password_post(request):
    current_password = request.POST['current_password']
    salt=Login.objects.get(id=request.session['lid']).salt
    current_password=salt+current_password
    current_password = hashlib.md5(current_password.encode('utf-8')).hexdigest()

    log=Login.objects.get(id=request.session['lid'])
    # logpass=Login.objects.get(id=request.session['lid']).password
    logpass=log.password

    if logpass==current_password:
        new_password=request.POST['password']

        # Ensure the new password is not the same as the current password
        new_salt=''.join(random.choices(string.ascii_letters,k=7))
        new_password=new_salt+new_password
        new_password = hashlib.md5(new_password.encode('utf-8')).hexdigest()
        if new_password == logpass:
            return HttpResponse('''<script>alert("New password cannot be the same as the current password! Please try again.");window.location="/seller_profile/"</script>''')
        
        # Update password and salt
        log.salt=new_salt  
        log.password=new_password
        log.save()
        
        return HttpResponse('''<script>alert("Password changed successfully.");window.location="/seller_profile/"</script>''')
    else:
        return HttpResponse('''<script>alert("Current password incorrect! Please try again.");window.location="/seller_profile/"</script>''')
    
def add_product(request):
    subc=SubCategory.objects.all()
    slr=Seller.objects.all()
    return render(request,"add_product.html",{'subcategory' : subc, 'seller' : slr})

def add_product_post(request):
    name=request.POST['name']
    brand=request.POST['brand']
    price=request.POST['price']
    desc=request.POST['desc']
    instock=request.POST['instock']
    subcategory=request.POST['subcategory']
    thumbnail=request.FILES['thumbnail']
    images = request.FILES.getlist('image')
    videos=request.FILES.getlist('video',None) #optional
    prod=Product(
        name=name,
        brand=brand,
        price=price,
        desc=desc,
        instock=instock,
        subcategory_id=subcategory,
        thumbnail=thumbnail,
        seller=Seller.objects.get(login_id=request.session['lid'])
    )
    prod.save()

    for img in images:
        product_img=ProductImg(image=img)
        product_img.save()
        prod.images.add(product_img)

    for vid in videos:
        product_vid=ProductVid(video=vid)
        product_vid.save()
        prod.videos.add(product_vid)    

    prod.save()

    return HttpResponse('''<script>alert("Product added succesfully.");window.location="/add_product/"</script>''')

def view_products(request):
    seller = Seller.objects.get(login=request.session['lid'])
    products = Product.objects.filter(seller=seller)
    return render(request,"view_products.html", {'products' : products})

def edit_product(request,id):
    editproduct=Product.objects.get(id=id)
    subc=SubCategory.objects.all()
    slr=Seller.objects.all()
    return render(request,"edit_product.html",{'product' : editproduct, 'subcategory' : subc, 'seller' : slr})

def edit_product_post(request):
    id=request.POST["id"]
    pr=Product.objects.get(id=id)

    subcategory_id=request.POST['subcategory']
    sbc=SubCategory.objects.get(id=subcategory_id)

    pr.name=request.POST['name']
    pr.brand=request.POST['brand']
    pr.price=request.POST['price']
    pr.desc=request.POST['desc']
    pr.subcategory=sbc

    if 'thumbnail' in request.FILES:
        pr.thumbnail=request.FILES['thumbnail']
    if 'image' in request.FILES:
        pr.images.set(request.FILES.getlist('image'))
    if 'video' in request.FILES:    
        pr.videos.set(request.FILES.getlist('video',None))

    pr.save()
    return HttpResponse('''<script>alert("Product updated successfully.");window.location="/view_products/"</script>''')  

def delete_product(request,id):
    product=Product.objects.get(id=id).delete()
    return HttpResponse('''<script>alert("Product deleted successfully.");window.location="/view_products/"</script>''')

def add_offer(request):
    product=Product.objects.all()
    return render(request,"add_offer.html",{'product':product})

def add_offer_post(request):
    product = request.POST.get('product', '').strip()
    ccoupon = request.POST.get('coupon', '').strip()
    cdiscount = request.POST.get('cdiscount', '').strip()
    discount = request.POST.get('discount', '').strip()
    sdate = request.POST.get('sdate', '').strip()
    edate = request.POST.get('edate', '').strip()

    # Validate discount value
    if discount:
        try:
            discount = float(discount)
            if not (0 <= discount <= 100):
                return HttpResponse(
                    '''<script>alert("Discount must be between 0 and 100.");window.location="/add_offer/"</script>'''
                )
        except ValueError:
            return HttpResponse(
                '''<script>alert("Invalid discount value.");window.location="/add_offer/"</script>'''
            )
    else:
        discount = 0  # If no discount is provided, set to 0

    # Ensure at least one of coupon or offer is filled
    if not ccoupon and discount == 0:
        return HttpResponse(
            '''<script>alert("Either a coupon or an offer must be provided.");window.location="/add_offer/"</script>'''
        )

    # Validate date range
    if datetime.strptime(edate, '%Y-%m-%d') < datetime.strptime(sdate, '%Y-%m-%d'):
        return HttpResponse('''<script>alert("End date cannot be earlier than start date.");window.location="/add_offer/"</script>''')

    # Save offer if discount is provided
    if discount > 0 or ccoupon:  # Create an offer even if no direct discount is provided, but a coupon exists
        off = Offer(
            discount=discount,
            sdate=sdate,
            edate=edate,
            product=Product.objects.get(id=product)
        )
        off.save()

    # Save coupon if coupon details are provided
    if ccoupon:
        try:
            cdiscount = float(cdiscount) if cdiscount else 0
            coupn = Coupon()
            coupn.coupon = ccoupon
            coupn.cdiscount = cdiscount
            coupn.product = Product.objects.get(id=product)
            coupn.save()
        except ValueError:
            return HttpResponse(
                '''<script>alert("Invalid coupon discount value.");window.location="/add_offer/"</script>'''
            )

    return HttpResponse('''<script>alert("Offer added successfully.");window.location="/seller_dashboard/"</script>''')

def view_offers(request):
    seller = Seller.objects.get(login=request.session['lid'])
    offers = Offer.objects.filter(product__seller=seller).prefetch_related('product__coupon_set')
    for offer in offers:
        original_price = offer.product.price
        offer_discount = offer.discount if offer.discount is not None else 0

        # Get the coupon discount if a coupon exists
        coupon = offer.product.coupon_set.first()  # Fetch the first coupon
        coupon_discount = coupon.cdiscount if coupon else 0  # Handle case where no coupon exists

        # Calculate the final price with both offer and coupon discounts
        final_price = original_price - (original_price * (offer_discount + coupon_discount) / 100)
        offer.final_price = round(final_price)

    return render(request, "view_offers.html", {'offers': offers})



def edit_offer(request,id):
    offer=Offer.objects.get(id=id)
    offer.sdate = offer.sdate.strftime('%Y-%m-%d')
    offer.edate = offer.edate.strftime('%Y-%m-%d')
    product =offer.product.id
    coupons=Coupon.objects.filter(product_id=product).first()
    return render(request,"edit_offer.html",{'offer':offer, 'coupon': coupons})

def edit_offer_post(request):
    id = request.POST["id"]
    offer = Offer.objects.get(id=id)

    # Fetch the product by name
    product_name = request.POST.get('product', '').strip()
    try:
        prd = Product.objects.get(name=product_name).id
    except Product.DoesNotExist:
        return HttpResponse(
            '''<script>alert("Product not found.");window.location="/view_offers/"</script>'''
        )

    # Update or create the coupon for the product
    coupon = Coupon.objects.filter(product_id=prd).first()
    ccoupon = request.POST.get('coupon', '').strip()
    cdiscount = request.POST.get('cdiscount', '').strip()

    if coupon:  # If a coupon exists, update it
        coupon.coupon = ccoupon
        try:
            coupon.cdiscount = float(cdiscount) if cdiscount else 0
        except ValueError:
            return HttpResponse(
                '''<script>alert("Invalid coupon discount value.");window.location="/view_offers/"</script>'''
            )
        coupon.save()
    elif ccoupon or cdiscount:  # Create a new coupon if details are provided
        try:
            cdiscount_value = float(cdiscount) if cdiscount else 0
            coupon = Coupon(
                product_id=prd,
                coupon=ccoupon,
                cdiscount=cdiscount_value
            )
            coupon.save()
        except ValueError:
            return HttpResponse(
                '''<script>alert("Invalid coupon discount value.");window.location="/view_offers/"</script>'''
            )

    # Update the offer
    try:
        discount = float(request.POST.get('discount', '0').strip())
        if not (0 <= discount <= 100):
            return HttpResponse(
                '''<script>alert("Discount must be between 0 and 100.");window.location="/view_offers/"</script>'''
            )
    except ValueError:
        return HttpResponse(
            '''<script>alert("Invalid discount value.");window.location="/view_offers/"</script>'''
        )

    sdate = request.POST.get('sdate', '').strip()
    edate = request.POST.get('edate', '').strip()
    if datetime.strptime(edate, '%Y-%m-%d') < datetime.strptime(sdate, '%Y-%m-%d'):
        return HttpResponse(
            '''<script>alert("End date cannot be earlier than start date.");window.location="/view_offers/"</script>'''
        )

    offer.product_id = prd
    offer.discount = discount
    offer.sdate = sdate
    offer.edate = edate
    offer.save()

    return HttpResponse(
        '''<script>alert("Offer updated successfully.");window.location="/view_offers/"</script>'''
    )

#CUSTOMER:

def remove_offer(request,id):
    offer=Offer.objects.get(id=id).delete()
    return HttpResponse('''<script>alert("offer removed successfully.");window.location="/view_offers/"</script>''')

def shop(request):
    user = Signup.objects.get(login=request.session['lid'])
    categories = Category.objects.all()
    brands = Product.objects.values_list('brand', flat=True).distinct()  # Get distinct brands
    subcategories = SubCategory.objects.all().prefetch_related(
        Prefetch('product_set', queryset=Product.objects.select_related('subcategory__category'))
    )
    offers = Offer.objects.all()


    products_by_category = {}

    for category in categories:
        category_subcategories = subcategories.filter(category=category)
        category_products = {}

        for subcategory in category_subcategories:
            products = subcategory.product_set.all()

            # Add discount prices and ratings
            for product in products:
                offer = offers.filter(product=product).first()
                product.discounted_price = round(product.price - (product.price * offer.discount / 100)) if offer else product.price

                reviews = Review.objects.filter(product=product)
                if reviews.exists():
                    product.overall_rating = round(reviews.aggregate(Avg('rating'))['rating__avg'], 1)
                    product.total_ratings = reviews.count()
                    product.total_reviews = reviews.count()
                else:
                    product.overall_rating = 0.0
                    product.total_ratings = 0
                    product.total_reviews = 0

            category_products[subcategory] = products
        
        products_by_category[category] = category_products

    return render(request, "shop.html", {
        'categories': categories,
        'brands': brands,  # Pass brands to template
        'products_by_category': products_by_category,
        'selected_categories': [],  # No filters applied initially
        'selected_subcategories': [],
        'selected_brands': [],  # No brand filters applied initially

    })


def category(request, id):
    user = Signup.objects.get(login=request.session['lid'])
    category = get_object_or_404(Category, id=id)
    subcategories = SubCategory.objects.filter(category=category).prefetch_related(
        Prefetch('product_set', queryset=Product.objects.select_related('subcategory__category'))
    )
    offers = Offer.objects.all()

    products_by_subcategory = {}

    for subcategory in subcategories:
        products = subcategory.product_set.all()

        for product in products:
            offer = offers.filter(product=product).first()
            product.discounted_price = round(product.price - (product.price * offer.discount / 100)) if offer else product.price

            reviews = Review.objects.filter(product=product)
            if reviews.exists():
                product.overall_rating = round(reviews.aggregate(Avg('rating'))['rating__avg'], 1)
                product.total_ratings = reviews.count()
                product.total_reviews = reviews.count()
            else:
                product.overall_rating = 0.0
                product.total_ratings = 0
                product.total_reviews = 0

        products_by_subcategory[subcategory] = products

    brands = Product.objects.filter(subcategory__in=subcategories).values_list('brand', flat=True).distinct()

    search_history = []
    if user:
        search_history = SearchHistory.objects.filter(user=user).order_by('-searched_at')[:10]

    return render(request, "category.html", {
        'category': category,
        'subcategories': subcategories,
        'brands': brands,
        'products_by_subcategory': products_by_subcategory,
        'selected_subcategories': [],
        'selected_brands': [],
        'search_history':search_history,
    })


def filter_products(request):
    categories = Category.objects.all()
    selected_categories = request.GET.getlist('categories')
    selected_subcategories = request.GET.getlist('subcategories')
    selected_brands = request.GET.getlist('brands')
    selected_ratings = request.GET.getlist('ratings')

    # Get min_price and max_price from the request
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Check if any filters are applied
    any_filters_applied = (
        selected_categories or
        selected_subcategories or
        selected_brands or
        selected_ratings or
        min_price or
        max_price
    )

    # Handle empty values and provide defaults
    try:
        min_price = float(min_price) if min_price else 1000  # Default minimum price
    except ValueError:
        min_price = 1000  # Fallback to default if conversion fails

    try:
        max_price = float(max_price) if max_price else 200000  # Default maximum price
    except ValueError:
        max_price = 200000  # Fallback to default if conversion fails

    # Fetch all products
    products = Product.objects.all()

    # Filter by price range
    products = products.filter(price__gte=min_price, price__lte=max_price)

    # Filter by selected categories (via subcategory)
    if selected_categories:
        products = products.filter(subcategory__category__in=selected_categories)

    # Filter by selected subcategories
    if selected_subcategories:
        products = products.filter(subcategory__in=selected_subcategories)

    # Annotate products with their average rating
    products = products.annotate(avg_rating=Avg('reviews__rating'))

    # Filter by selected brand(s)
    if selected_brands:
        products = products.filter(brand__in=selected_brands)

    # Filter by selected ratings
    if selected_ratings:
        rating_filters = Q()
        for rating_range in selected_ratings:
            min_rating, max_rating = map(float, rating_range.split('-'))
            rating_filters |= Q(avg_rating__gte=min_rating, avg_rating__lt=max_rating)
        
        products = products.filter(rating_filters).distinct()

    # Get the subcategories of the filtered products
    subcategories = SubCategory.objects.filter(product__in=products).distinct()

    # Get the categories of those subcategories
    categories = Category.objects.filter(subcategory__in=subcategories).distinct()

    # Organize products into categories and subcategories
    products_by_category = {}
    for category in categories:
        category_subcategories = subcategories.filter(category=category)
        if not category_subcategories.exists():
            continue

        category_products = {}
        for subcategory in category_subcategories:
            products_in_subcategory = products.filter(subcategory=subcategory)

            # Add discount prices and ratings
            for product in products_in_subcategory:
                offer = Offer.objects.filter(product=product).first()
                product.discounted_price = round(product.price - (product.price * offer.discount / 100)) if offer else product.price

                product.overall_rating = round(product.avg_rating, 1) if product.avg_rating else 0.0
                product.total_ratings = Review.objects.filter(product=product).count()
                product.total_reviews = product.total_ratings

            category_products[subcategory] = products_in_subcategory

        products_by_category[category] = category_products

    # Fetch available brands
    brands = Product.objects.values_list('brand', flat=True).distinct()

    return render(request, 'shop.html', {
        'categories': categories,
        'brands': brands,
        'products_by_category': products_by_category,
        'selected_categories': selected_categories,
        'selected_subcategories': selected_subcategories,
        'selected_brands': selected_brands,
        'min_price': min_price,
        'max_price': max_price,        
        'selected_ratings': selected_ratings,
        'any_filters_applied': any_filters_applied,
    })

def filter_category_products(request, category_id):
    category = Category.objects.get(id=category_id)
    
    # Get selected filters from the request
    selected_subcategories = request.GET.getlist('subcategories')
    selected_brands = request.GET.getlist('brands')
    selected_ratings = request.GET.getlist('ratings')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Check if any filters are applied
    any_filters_applied = (
        selected_subcategories or
        selected_brands or
        selected_ratings or
        min_price or
        max_price
    )

    # Handle empty values and provide defaults for price
    try:
        min_price = float(min_price) if min_price else 1000  # Default minimum price
    except ValueError:
        min_price = 1000  # Fallback to default if conversion fails

    try:
        max_price = float(max_price) if max_price else 200000  # Default maximum price
    except ValueError:
        max_price = 200000  # Fallback to default if conversion fails

    # Fetch all products within the selected category
    products = Product.objects.filter(subcategory__category=category)

    # Filter by price range
    products = products.filter(price__gte=min_price, price__lte=max_price)

    # Filter by selected subcategories
    if selected_subcategories:
        products = products.filter(subcategory__in=selected_subcategories)

    # Annotate products with their average rating
    products = products.annotate(avg_rating=Avg('reviews__rating'))

    # Filter by selected brand(s)
    if selected_brands:
        products = products.filter(brand__in=selected_brands)

    # Filter by selected ratings
    if selected_ratings:
        rating_filters = Q()
        for rating_range in selected_ratings:
            min_rating, max_rating = map(float, rating_range.split('-'))
            rating_filters |= Q(avg_rating__gte=min_rating, avg_rating__lt=max_rating)
        products = products.filter(rating_filters).distinct()

    # Get the subcategories of the filtered products
    filtered_subcategories = SubCategory.objects.filter(product__in=products).distinct()

    # Organize products into subcategories
    products_by_subcategory = {}
    for subcategory in filtered_subcategories:
        products_in_subcategory = products.filter(subcategory=subcategory)

        # Add discount prices and ratings
        for product in products_in_subcategory:
            offer = Offer.objects.filter(product=product).first()
            product.discounted_price = round(product.price - (product.price * offer.discount / 100)) if offer else product.price

            product.overall_rating = round(product.avg_rating, 1) if product.avg_rating else 0.0
            product.total_ratings = Review.objects.filter(product=product).count()
            product.total_reviews = product.total_ratings

        products_by_subcategory[subcategory] = products_in_subcategory

    # Fetch ALL subcategories for the filter pane (not just the filtered ones)
    all_subcategories = SubCategory.objects.filter(category=category).distinct()

    # Fetch ALL brands for the filter pane (not just the filtered ones)
    all_brands = Product.objects.filter(subcategory__category=category).values_list('brand', flat=True).distinct()

    return render(request, 'category.html', {
        'category': category,
        'subcategories': all_subcategories,  # Pass ALL subcategories
        'brands': all_brands,  # Pass ALL brands
        'products_by_subcategory': products_by_subcategory,
        'selected_subcategories': selected_subcategories,
        'selected_brands': selected_brands,
        'min_price': min_price,
        'max_price': max_price,
        'selected_ratings': selected_ratings,
        'any_filters_applied': any_filters_applied,
    })

def subcategory(request, subcategory_id):
    user = Signup.objects.get(login=request.session['lid'])
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    offers = Offer.objects.all()
    products = subcategory.product_set.all()

    for product in products:
        offer = offers.filter(product=product).first()
        product.discounted_price = round(product.price - (product.price * offer.discount / 100)) if offer else product.price

        reviews = Review.objects.filter(product=product)
        if reviews.exists():
            product.overall_rating = round(reviews.aggregate(Avg('rating'))['rating__avg'], 1)
            product.total_ratings = reviews.count()
            product.total_reviews = reviews.count()
        else:
            product.overall_rating = 0.0
            product.total_ratings = 0
            product.total_reviews = 0

    brands = products.values_list('brand', flat=True).distinct()

    search_history = []
    if user:
        search_history = SearchHistory.objects.filter(user=user).order_by('-searched_at')[:10]

    return render(request, "subcategory.html", {
        'subcategory': subcategory,
        'products': products,
        'brands': brands,
        'selected_brands': [],
        'selected_ratings': [],
        'min_price': 1000,  # Default minimum price
        'max_price': 200000,  # Default maximum price
        'any_filters_applied': False,
        'search_history':search_history,
    })

def filter_subcategory_products(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    
    # Get selected filters from the request
    selected_brands = request.GET.getlist('brands')
    selected_ratings = request.GET.getlist('ratings')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Check if any filters are applied
    any_filters_applied = (
        selected_brands or
        selected_ratings or
        min_price or
        max_price
    )

    # Handle empty values and provide defaults for price
    try:
        min_price = float(min_price) if min_price else 1000  # Default minimum price
    except ValueError:
        min_price = 1000  # Fallback to default if conversion fails

    try:
        max_price = float(max_price) if max_price else 200000  # Default maximum price
    except ValueError:
        max_price = 200000  # Fallback to default if conversion fails

    # Fetch all products within the selected subcategory
    products = Product.objects.filter(subcategory=subcategory)

    # Filter by price range
    products = products.filter(price__gte=min_price, price__lte=max_price)

    # Filter by selected brand(s)
    if selected_brands:
        products = products.filter(brand__in=selected_brands)

    # Filter by selected ratings
    if selected_ratings:
        rating_filters = Q()
        for rating_range in selected_ratings:
            min_rating, max_rating = map(float, rating_range.split('-'))
            rating_filters |= Q(avg_rating__gte=min_rating, avg_rating__lt=max_rating)
        products = products.filter(rating_filters).distinct()

    # Add discount prices and ratings
    offers = Offer.objects.all()
    for product in products:
        offer = offers.filter(product=product).first()
        product.discounted_price = round(product.price - (product.price * offer.discount / 100)) if offer else product.price

        reviews = Review.objects.filter(product=product)
        if reviews.exists():
            product.overall_rating = round(reviews.aggregate(Avg('rating'))['rating__avg'], 1)
            product.total_ratings = reviews.count()
            product.total_reviews = reviews.count()
        else:
            product.overall_rating = 0.0
            product.total_ratings = 0
            product.total_reviews = 0

    # Fetch ALL brands for the filter pane (not just the filtered ones)
    all_brands = Product.objects.filter(subcategory=subcategory).values_list('brand', flat=True).distinct()

    return render(request, 'subcategory.html', {
        'subcategory': subcategory,
        'products': products,
        'brands': all_brands,
        'selected_brands': selected_brands,
        'selected_ratings': selected_ratings,
        'min_price': min_price,
        'max_price': max_price,
        'any_filters_applied': any_filters_applied,
    })

def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    suggestions = []

    if query:
        # Fetch product suggestions
        products = Product.objects.filter(
            Q(name__icontains=query)
        ).values_list('name', flat=True)[:5]
        suggestions.extend([f"Product: {name}" for name in products])

        # Fetch category suggestions
        categories = Category.objects.filter(
            Q(name__icontains=query)
        ).values_list('name', flat=True)[:5]
        suggestions.extend([f"Category: {name}" for name in categories])

        # Fetch subcategory suggestions
        subcategories = SubCategory.objects.filter(
            Q(name__icontains=query)
        ).values_list('name', flat=True)[:5]
        suggestions.extend([f"Subcategory: {name}" for name in subcategories])

        # Fetch brand suggestions (assuming 'brand' is a field in the Product model)
        brands = Product.objects.filter(
            Q(brand__icontains=query)
        ).values_list('brand', flat=True).distinct()[:5]
        suggestions.extend([f"Brand: {name}" for name in brands])

        suggestions = suggestions[:10]  # Limit to 10 total suggestions

    return JsonResponse({'suggestions': suggestions})

def search(request):
    query = request.GET.get('q', '')
    try:
        user = Signup.objects.get(login=request.session['lid'])
    except (Signup.DoesNotExist, KeyError):
        user = None
       
    # Save the search query if the user is authenticated and the query is not already in the history
    search_history = []
    if user and query:
        if not SearchHistory.objects.filter(user=user, query=query).exists():
            SearchHistory.objects.create(user=user, query=query, searched_at=now())
        search_history = SearchHistory.objects.filter(user=user).order_by('-searched_at')[:10]

    # Fetch all products based on search query
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(subcategory__name__icontains=query) |
            Q(subcategory__category__name__icontains=query)
        ).distinct()
    else:
        products = Product.objects.none()

    # Apply filters
    selected_categories = request.GET.getlist('categories', [])
    selected_subcategories = request.GET.getlist('subcategories', [])
    selected_brands = request.GET.getlist('brands', [])
    selected_ratings = request.GET.getlist('ratings', [])
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    # Check if any filters are applied
    any_filters_applied = (
        selected_categories or
        selected_subcategories or
        selected_brands or
        selected_ratings or
        min_price or
        max_price
    )

    # Handle empty values and provide defaults for price
    try:
        min_price = float(min_price) if min_price else 0
    except ValueError:
        min_price = 0

    try:
        max_price = float(max_price) if max_price else 200000
    except ValueError:
        max_price = 200000

    # Apply filters
    if selected_categories:
        products = products.filter(subcategory__category__in=selected_categories)
    if selected_subcategories:
        products = products.filter(subcategory__in=selected_subcategories)
    if selected_brands:
        products = products.filter(brand__in=selected_brands)
    if selected_ratings:
        rating_filters = Q()
        for rating_range in selected_ratings:
            min_rating, max_rating = map(float, rating_range.split('-'))
            rating_filters |= Q(avg_rating__gte=min_rating, avg_rating__lt=max_rating)
        products = products.annotate(avg_rating=Avg('reviews__rating')).filter(rating_filters).distinct()
    if min_price or max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    # Add discount prices and ratings
    offers = Offer.objects.all()
    for product in products:
        offer = offers.filter(product=product).first()
        product.discounted_price = round(product.price - (product.price * offer.discount / 100)) if offer else product.price

        reviews = Review.objects.filter(product=product)
        if reviews.exists():
            product.overall_rating = round(reviews.aggregate(Avg('rating'))['rating__avg'], 1)
            product.total_ratings = reviews.count()
            product.total_reviews = reviews.count()
        else:
            product.overall_rating = 0.0
            product.total_ratings = 0
            product.total_reviews = 0

    # Fetch all categories, subcategories, and brands for the filter pane
    categories = Category.objects.all()
    brands = Product.objects.values_list('brand', flat=True).distinct()

    return render(request, 'search_results.html', {
        'search_history': search_history,
        'products': products,
        'query': query,
        'categories': categories,
        'brands': brands,
        'selected_categories': selected_categories,
        'selected_subcategories': selected_subcategories,
        'selected_brands': selected_brands,
        'selected_ratings': selected_ratings,
        'min_price': min_price,
        'max_price': max_price,
        'any_filters_applied': any_filters_applied,
    })

@method_decorator(csrf_exempt, name='dispatch')
class DeleteSearchHistory(View):
    def post(self, request, history_id):
        try:
            user = Signup.objects.get(login=request.session['lid'])
            search_history = SearchHistory.objects.get(id=history_id, user=user)
            search_history.delete()
            return JsonResponse({'status': 'success'})
        except (Signup.DoesNotExist, KeyError, SearchHistory.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ClearAllSearchHistory(View):
    def post(self, request):
        try:
            user = Signup.objects.get(login=request.session['lid'])
            SearchHistory.objects.filter(user=user).delete()
            return JsonResponse({'status': 'success'})
        except (Signup.DoesNotExist, KeyError):
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def single_product(request,p_id):
    product = Product.objects.get(id=p_id)
    offers = Offer.objects.filter(product=product)
    reviews = Review.objects.filter(product=product)

    for offer in offers:
        original_price=offer.product.price
        discount=offer.discount
        offer.final_price=round(original_price-(original_price*discount/100))
    total_images = product.images.count()
    
    if reviews.exists():
        total_reviews = reviews.count()
        total_ratings = reviews.count()
        overall_rating = round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)

        # Count reviews for each star rating
        star_counts = {
            5: reviews.filter(rating__gte=4.5).count(),
            4: reviews.filter(rating__gte=3.5, rating__lt=4.5).count(),
            3: reviews.filter(rating__gte=2.5, rating__lt=3.5).count(),
            2: reviews.filter(rating__gte=1.5, rating__lt=2.5).count(),
            1: reviews.filter(rating__lt=1.5).count(),
        }  
    else:
        total_reviews = 0
        total_ratings = 0
        overall_rating = 0.0
        star_counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}

    # Check stock availability
    is_in_stock = product.instock > 1    

    context = {
        'product': product,
        'offers':offers,
        'total_images': total_images,
        'reviews': reviews,
        'overall_rating': overall_rating,
        'total_reviews': total_reviews,
        'total_ratings': total_ratings,
        'star_counts': star_counts,
        'is_in_stock':is_in_stock,
    }            
    return render(request,"single-product.html", context)

def review_post(request,p_id):
    product = Product.objects.get(id=p_id)
    user = Signup.objects.get(login=request.session['lid'])
    rating=request.POST['rating']
    comment=request.POST['comment']
    pdate=datetime.now()

    if not rating:
        return HttpResponse('''<script>alert("Please provide a rating.");window.history.back();</script>''')

    rw=Review(
        product_id=p_id,
        user=user,
        rating=rating,
        comment=comment,
        pdate=pdate
    )
    rw.save()
    return HttpResponse('''<script>alert("Review posted successfully!.");window.location="/category/"</script>''')

def add_to_wishlist(request):
    user_id = request.session['lid']
    p_id=request.POST['p_id']
    product = Product.objects.get(id=p_id)
    date = datetime.now()

    wl=Wishlist(
        user_id=user_id,
        product=product,
        date=date,
    )
    wl.save()
    return HttpResponse('''<script>alert("Product added to wishlist successfully!.");window.location="/wishlist/"</script>''')

def wishlist(request):
    user = Signup.objects.get(login=request.session['lid'])
    wishlist_items = Wishlist.objects.filter(user=user)
    offers = Offer.objects.all()

    # Prepare the wishlist with discounted prices
    wishlist_data = []
    # Add discounted prices to each product
    for item in wishlist_items:
        product = item.product
        offer = offers.filter(product_id=product.id).first()  # Get the offer for the product
        if offer:
            discounted_price = round(product.price - (product.price * offer.discount / 100))
        else:
            discounted_price = product.price  # No discount applied

        # Append product data along with discounted price to the list
        wishlist_data.append({
            'id': item.id,
            'product': product,
            'discounted_price': discounted_price,
        })
    
    search_history = []
    if user:
        search_history = SearchHistory.objects.filter(user=user).order_by('-searched_at')[:10]
       
    return render(request,"wishlist.html",{'wishlist': wishlist_data, 'search_history':search_history})

def remove_wishlist_item(request,id):
    wishlist_item=Wishlist.objects.get(id=id).delete()
    return HttpResponse('''<script>alert("item removed from wishlist successfully.");window.location="/wishlist/"</script>''')

def add_to_cart(request):
    user = request.session['lid']
    p_id = request.POST['p_id']
    product = Product.objects.get(id=p_id)
    quantity = int(request.POST["qty"])
    date = datetime.now()

    # Initialize discount_price with the product's original price
    discount_price = product.price

    offer = Offer.objects.filter(
        product=product,
        sdate__lte=date,
        edate__gte=date,
    ).first()

    if offer:
        discount_price = product.price * (1 - offer.discount / 100)
        total_amount = discount_price * quantity
    else:
        total_amount = product.price * quantity

    # Check if the cart item already exists
    cart_item = Cart.objects.filter(user__login_id=user, product_id=p_id).first()
    if cart_item:
        cart_item.quantity += quantity
        cart_item.amount = total_amount
        cart_item.offer = offer  # Update offer if applicable
        cart_item.save()
    else:
        ct = Cart(
            user=Signup.objects.get(login_id=user),
            product_id=p_id,
            amount=total_amount,
            date=date,
            quantity=quantity,
            offer=offer,
            offer_amount=discount_price
        )
        ct.save()
        request.session['cid'] = ct.id

    return HttpResponse('''<script>alert("Product added to cart successfully!");window.location="/cart/"</script>''')

# def cart(request):
#     user = Signup.objects.get(login=request.session['lid'])
#     cart_items = Cart.objects.filter(user=user)
#     applied_coupons = AppliedCoupon.objects.filter(user=user).select_related('coupon')

#     for item in cart_items:
#         # check for active offer:
#         offer = Offer.objects.filter(
#             product=item.product,
#             sdate__lte=datetime.now(),
#             edate__gte=datetime.now()
#         ).first()

#         if offer:
#             discount_price = round(item.product.price * (1 - offer.discount / 100),2)
#             item.final_amount = round(discount_price * item.quantity,2)
#         else:
#             item.final_amount = round(item.product.price * item.quantity,2)
#     total_price = sum(item.final_amount for item in cart_items)
#     return render(request,"cart.html",{"cart":cart_items, "total_price": total_price, "discount_price":discount_price, 'applied_coupons': applied_coupons})

def cart(request):
    user = Signup.objects.get(login=request.session['lid'])
    cart_items = Cart.objects.filter(user=user,status='Pending')
    applied_coupons = AppliedCoupon.objects.filter(user=user,status='Applied').select_related('coupon')

    # Initialize default values
    total_price = 0
    offer_amount = 0  # To avoid uninitialized variable error

    # If cart is empty, show no applied coupons
    if not cart_items.exists():
        applied_coupons = []  # An empty list will make the template show "No coupons applied yet."



    if cart_items.exists():
        for item in cart_items:
            # Check for active offer:
            offer = Offer.objects.filter(
                product=item.product,
                sdate__lte=datetime.now(),
                edate__gte=datetime.now()
            ).first()

            if offer:
                offer_amount = round(item.product.price * (1 - offer.discount / 100), 2)
            else:
                offer_amount = item.product.price

            # Check for applied coupon:
            if item.coupon_amount:
                final_price = round(item.coupon_amount * item.quantity, 2)
            else:
                final_price = round(offer_amount * item.quantity, 2)

            # Update the final amount
            item.final_amount = final_price

        total_price = sum(item.final_amount for item in cart_items)

    search_history = []
    if user:
        search_history = SearchHistory.objects.filter(user=user).order_by('-searched_at')[:10]
        

    return render(request, "cart.html", {
        "cart": cart_items,
        "total_price": total_price,
        "discount_price": offer_amount,
        "applied_coupons": applied_coupons,
        'search_history':search_history,
    })




# def apply_coupon(request,id):
#     user =Signup.objects.get(login_id=request.session['lid'])
#     cart_item = Cart.objects.get(id=id)
#     hh=Cart.objects.get(id=id).product.id
#     coupon_code = request.POST.get('coupon', '').strip()

#     if request.method == "POST" and coupon_code:
#         try:
#             coupon = Coupon.objects.get(product=hh, coupon=coupon_code)            
#         except Coupon.DoesNotExist:
#             return HttpResponse('''<script>alert("Invalid coupon code.");window.location="/cart/"</script>''')
            
#             # Check if the coupon is already applied
#         if AppliedCoupon.objects.filter(user=user, coupon=coupon).exists():
#             return HttpResponse('''<script>alert("Coupon already applied.");window.location="/cart/"</script>''')
            
#         # Apply the coupon
#         if cart_item.offer_amount:
#             discount_price = cart_item.offer_amount * (1 - coupon.cdiscount / 100)
#             cart_item.coupon_amount = round(discount_price, 2)
#             cart_item.save()
#         else:
#             discount_price = cart_item.amount * (1 - coupon.cdiscount / 100)
#             cart_item.coupon_amount = round(discount_price, 2)
#             cart_item.save()

#         # Mark coupon as applied
#         AppliedCoupon.objects.create(user=user, coupon=coupon)
#         return HttpResponse('''<script>alert("Coupon applied successfully!");window.location="/cart/"</script>''')
        
#     return HttpResponse('''<script>alert("Invalid request.");window.location="/cart/"</script>''')

from django.http import JsonResponse

def apply_coupon(request):
    if request.method == "POST":
        user = Signup.objects.get(login_id=request.session['lid'])
        product_id = request.POST.get('product_id')
        coupon_code = request.POST.get('coupon', '').strip()

        if not product_id or not coupon_code:
            return JsonResponse({'status': 'error', 'message': 'Please select a product and enter a coupon code.'})

        try:
            cart_item = Cart.objects.get(id=product_id, user=user)
            hh = cart_item.product.id
            coupon = Coupon.objects.get(product=hh, coupon=coupon_code)
        except (Cart.DoesNotExist, Coupon.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Invalid product or coupon code.'})

        # Check if the coupon is already applied
        if AppliedCoupon.objects.filter(user=user, coupon=coupon).exists():
            return JsonResponse({'status': 'error', 'message': 'Coupon already applied.'})

        # Calculate discount based on offer and coupon
        offer = Offer.objects.filter(
            product=cart_item.product,
            sdate__lte=datetime.now(),
            edate__gte=datetime.now()
        ).first()

        if offer:
            # Offer discount
            offer_amount = cart_item.product.price * (1 - offer.discount / 100)
        else:
            offer_amount = None

        # Coupon discount
        coupon_amount = cart_item.product.price * (1 - coupon.cdiscount / 100)

        # Final discount (prioritize coupon)
        final_discount = (cart_item.offer_amount or cart_item.amount) * (1 - coupon.cdiscount / 100)
        cart_item.coupon_amount = round(final_discount, 2)
        cart_item.save()

        # Mark coupon as applied
        AppliedCoupon.objects.create(user=user, coupon=coupon, status='Applied')
        return JsonResponse({'status': 'success', 'message': 'Coupon applied successfully!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})




    #     # Apply the coupon
    #     discount_price = (
    #         cart_item.offer_amount or cart_item.amount
    #     ) * (1 - coupon.cdiscount / 100)
    #     cart_item.coupon_amount = round(discount_price, 2)
    #     cart_item.save()

    #     # Mark coupon as applied
    #     AppliedCoupon.objects.create(user=user, coupon=coupon)
    #     return HttpResponse('''<script>alert("Coupon applied successfully!");window.location="/cart/"</script>''')

    # return HttpResponse('''<script>alert("Invalid request.");window.location="/cart/"</script>''')



# def update_quantity(request,id):
#     qtity = request.POST['qty']
#     cart=Cart.objects.get(id=id)
#     cart.quantity=  int(qtity)
#     cart.save()
#     return HttpResponse('''<script>alert("Quantity updated successfully!");window.location="/cart/"</script>''')

def update_quantity(request, id):
    if request.method == "POST":
        try:
            qtity = request.POST['qty']
            cart = Cart.objects.get(id=id)
            cart.quantity = int(qtity)
            cart.save()

            # Return a JSON response to indicate success
            return JsonResponse({"status": "success", "message": "Quantity updated successfully!"})
        except Cart.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Cart item not found!"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method!"})

def remove_item(request,id):
    user = Signup.objects.get(login_id=request.session['lid'])    
    rt=Cart.objects.get(id=id).product.id
    coupon=AppliedCoupon.objects.filter(user=user,coupon__product_id=rt).delete()
    cart=Cart.objects.get(id=id).delete()
    return HttpResponse('''<script>alert("item removed from cart successfully.");window.location="/cart/"</script>''')

def cart_post(request):
    user_id = request.session['lid']
    cart_id=request.POST['cart_id']
    # if Checkout.objects.filter(user_id=user_id).first():
    #     return HttpResponse('''<script>alert("Cart already submitted.");window.location="/cart/"</script>''')
    # else:
    total_str=request.POST['total']
    total = float(total_str.replace(',', ''))
    date = datetime.now()
    # Create a new Checkout object
    checkout = Checkout.objects.create(
        user=Signup.objects.get(id=user_id),
        total=total,
        payment_status='Pending',
        date=date
    )
    return HttpResponse('''<script>alert("Details submitted successfully.");window.location="/checkout/"</script>''')

def checkout(request):
    user_id = request.session['lid']
    signup_data = Signup.objects.filter(login_id=user_id).first()
    cart_items = Cart.objects.filter(user=user_id)

    # Prefill email and phone fields separately based on the signup method
    email_or_phone = signup_data.emailorphone
    email = phone = ''
    
    if '@' in email_or_phone:  # If email contains '@', treat it as an email
        email = email_or_phone
    else:  # Otherwise, treat it as a phone number
        phone = email_or_phone

    pincode = signup_data.pincode
    pincode_str = str(pincode).replace(',', '')

    for item in cart_items:
        # Check for active offer:
        offer = Offer.objects.filter(
            product=item.product,
            sdate__lte=datetime.now(),
            edate__gte=datetime.now()
        ).first()

        if offer:
            offer_amount = round(item.product.price * (1 - offer.discount / 100), 2)
        else:
            offer_amount = item.product.price

        # Check for applied coupon:
        if item.coupon_amount:
            final_price = round(item.coupon_amount * item.quantity, 2)
        else:
            final_price = round(offer_amount * item.quantity, 2)

        # Attach final amount to the item
        item.final_amount = final_price

    search_history = []
    if user_id:
        search_history = SearchHistory.objects.filter(user=user_id).order_by('-searched_at')[:10]

    # Total price for all cart items
    total_price = sum(item.final_amount for item in cart_items)
    order = Checkout.objects.filter(user_id=user_id).latest('date')
    return render(request,"checkout.html",{"user": signup_data,"cart": cart_items, 'order' : order,'email': email, 'phone': phone, 'pincode' : pincode_str, 'search_history':search_history})

def checkout_post(request):
    check_id=request.POST['check_id']
    # nn=Checkout.objects.filter(id=check_id).update(cart__status='Submitted')
    name=request.POST['name']
    phone=request.POST['phone']
    if not phone.isdigit() or len(phone) > 15:
        return HttpResponse('''<script>alert("Invalid phone number.");window.location="/checkout/"</script>''')
    email=request.POST['email']
    address=request.POST['address']
    state=request.POST['state']
    pincode=request.POST['pincode']
    notes = request.POST.get('notes', '')  # Default to empty string if 'notes' is missing
    payment_method=request.POST.get('payment_method')
    
    checkout = Checkout.objects.filter(id=check_id).first()
    if not checkout:
        return HttpResponse('''<script>alert("Invalid checkout ID.");window.location="/cart/"</script>''')

    # Check if payment has already been initiated or completed
    if checkout.payment_status in ['Initiated', 'Completed']:
        return HttpResponse('''<script>alert("Payment already in process or completed.");window.location="/cart/"</script>''')


    # checkout = Checkout.objects.get(id=check_id)
    # order_id = checkout.id
    dlv = DeliveryDetails(
        checkout=checkout,
        name=name,
        phone=phone,
        email=email,
        address=address,
        state=state,
        pincode=pincode,
        notes=notes,
        payment_method=payment_method
    )
    dlv.save()
    

    # Mark the applied coupons as NotApplied or delete them
    AppliedCoupon.objects.filter(user=checkout.user, status='Applied').update(status='Used')

    # Move cart items to OrderItem before deleting the cart
    cart_items = Cart.objects.filter(user=checkout.user, status='Pending')
    for cart_item in cart_items:
        # Check for active offer:
        offer = Offer.objects.filter(
            product=cart_item.product,
            sdate__lte=datetime.now(),
            edate__gte=datetime.now()
        ).first()

        if offer:
            offer_amount = round(cart_item.product.price * (1 - offer.discount / 100), 2)
        else:
            offer_amount = cart_item.product.price

        # Check for applied coupon:
        if cart_item.coupon_amount:
            final_price = round(cart_item.coupon_amount * cart_item.quantity, 2)
        else:
            final_price = round(offer_amount * cart_item.quantity, 2)

        OrderItem.objects.create(
            checkout=checkout,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=final_price
        )    

    cart_data = [
        {
            'product_id': cart_item.product.id,
            'product_name': cart_item.product.name,
            'quantity': cart_item.quantity,
            'price': float(final_price)
        }
        for cart_item in cart_items
    ]

    cart_items.delete()
    
    if payment_method=='upi':
        checkout.payment_status = 'Initiated'
        checkout.save()
        return HttpResponse('''<script>alert("Details submitted successfully. Redirecting to payment page.");window.location="/payment/{}/"</script>'''.format(checkout.id))
        
    return HttpResponse('''<script>alert("Order Successfull.");window.location="/orders_history/"</script>''')


razorpay_api_key = settings.RAZORPAY_API_KEY
razorpay_secret_key = settings.RAZORPAY_API_SECRET
razorpay_client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))

@csrf_exempt
def payment(request,check_id):
    product= get_object_or_404(Checkout, pk=check_id)
    # Amount to be paid (in paisa), you can change this dynamically based on your logic
    amount = int(product.total)
    # Create a Razorpay order (you need to implement this based on your logic)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1', # Auto-capture payment
    }
    # Create an order
    order = razorpay_client.order.create(data=order_data)
    print(order)
    callback_url = 'paymenthandler/'
    context = {
        'razorpay_api_key': razorpay_api_key,
        'amount': amount,
        'currency': order_data['currency'],
        'order_id': order['id'],
        'check_id':check_id,
        'callback_url':callback_url
    }
    return render(request, 'payment.html', context)

def payment_post(request):
    amount = request.POST['amount']
    checkout_id = request.POST['checkout_id']
    payment = Payment(
        amount=amount,
        checkout_id=checkout_id,
        date = datetime.now()
    )
    cc=Checkout.objects.get(id=checkout_id)
    cc.payment_status= 'Completed'
    cc.save()
    payment.save()


    return HttpResponse('''<script>alert("Payment successfull! Thanks for Shopping with us!");window.location="/orders_history/"</script>''')


def orders_history(request):
    # orders = DeliveryDetails.objects.all()
    # order_items = OrderItem.objects.all()
    user = Signup.objects.get(login=request.session['lid'])
    orders = DeliveryDetails.objects.filter(checkout__user=user).prefetch_related(
        Prefetch('checkout__order_items', queryset=OrderItem.objects.select_related('product'))
    )
    # Save the search query if the user is authenticated    
    search_history = []
    if user:
        search_history = SearchHistory.objects.filter(user=user).order_by('-searched_at')[:10]
    return render(request,"orders_history.html",{'orders':orders, 'search_history':search_history}) 

def order_details(request, id):
    user = Signup.objects.get(login=request.session['lid'])
    checkout = Checkout.objects.get(id=id, user=user)
    order_items = OrderItem.objects.filter(checkout=checkout).prefetch_related('returneditems_set')

    remaining_days = None

    if checkout.delivered_at:
        time_difference = now() - checkout.delivered_at
        remaining_days = 7 - time_difference.days

    # return_status= ReturnedItems.objects.get(order=order_items).status

    # Save the search query if the user is authenticated    
    search_history = []
    if user:
        search_history = SearchHistory.objects.filter(user=user).order_by('-searched_at')[:10]

    return render(request, "order_details.html", {
        'orders': order_items,
        'date': checkout.date,
        'c_id': checkout.id,
        'order_total': checkout.total,
        'payment_status': checkout.payment_status,
        'delivery_status': checkout.delivery_status,
        # 'return_status': return_status,
        'checkout': checkout,
        'remaining_days': remaining_days,
        'search_history':search_history,
    })

def cancel_order(request,id):
    # Get the order and update the delivery status
    order = Checkout.objects.get(id=id)
    order.delivery_status = "Cancelled"
    order.save()

    # Calculate the new subtotal for the user
    user = order.user
    remaining_orders = Checkout.objects.filter(user=user, delivery_status__in=["Pending", "Initiated", "Completed"])
    new_subtotal = sum(order.total for order in remaining_orders)
    
    return HttpResponse('''<script>alert("Order cancelled successfully.");window.location="/orders_history/"</script>''')
        
#SELLER:
def view_orders(request):
    # orders = DeliveryDetails.objects.prefetch_related(
    #     Prefetch('checkout__order_items', queryset=OrderItem.objects.select_related('product'))
    # )
    seller = Seller.objects.get(login=request.session['lid'])
    seller_products = Product.objects.filter(seller=seller)
    
    # Fetch orders (Checkout) that contain the seller's products
    orders = Checkout.objects.filter(order_items__product__in=seller_products).distinct()
    
    # Fetch customer details for each order
    order_details = []
    for order in orders:
        # Get the delivery details for the order
        delivery_details = DeliveryDetails.objects.get(checkout=order)
        order_details.append({
            'order': order,
            'delivery_details': delivery_details,
            'payment_method': delivery_details.payment_method,
        })
    return render(request, 'view_orders.html', {
        'order_details': order_details,
    })

def view_order_details(request,id):
    seller = Seller.objects.get(login=request.session['lid'])
    seller_products = Product.objects.filter(seller=seller)
    
    # Fetch the specific order (Checkout) by its ID
    order = get_object_or_404(Checkout, id=id)
    
    # Fetch order items and delivery details for the selected order
    order_items = OrderItem.objects.filter(checkout=order)  # All items in this order
    delivery_details = DeliveryDetails.objects.get(checkout=order)
    
    return render(request, "view_order_details.html", {
        'order': order,
        'order_items': order_items,
        'delivery_details': delivery_details,
        'date': order.date,
        'payment_status': order.payment_status,
        'delivery_status': order.delivery_status,
        'order_total': order.total,
    })

# def order_status(request,id,action):
#     # Get the order and update the delivery status
#     order = Checkout.objects.get(id=id)
#     # Check the action and update the delivery status
#     if action == 'dispatch':
#         # If the action is 'dispatch', update the delivery status to 'Dispatched'
#         if order.delivery_status != 'Dispatched':
#             # Loop through all OrderItem entries related to this checkout
#             for item in order.order_items.all():
#                 product = item.product
#                 # Reduce the stock of the product
#                 if product.instock >= item.quantity:
#                     product.instock -= item.quantity
#                     product.save()
#                 else:
#                     return HttpResponse(f'''<script>alert("Not enough stock for {product.name}."); window.location="/view_orders/";</script>''')

#             order.delivery_status = 'Dispatched'
#             message = 'Order dispatched successfully.'
#         else:
#             message = 'Order has already been dispatched.'
#     elif action == 'transit':
#         # If the action is 'transit', check if the order is already dispatched
#         if order.delivery_status == 'Dispatched':
#             order.delivery_status = 'In Transit'
#             message = 'Order is now in transit.'
#         else:
#             message = 'Dispatch the order first.'
#     else:
#         message = 'Invalid action.'
#     order.save()
    
#     return HttpResponse(f'''<script>alert("{message}"); window.location="/view_orders/";</script>''')


def order_status(request, id, action):
    # Get the order and update the delivery status
    order = Checkout.objects.get(id=id)
    message = ''

    if action == 'dispatch':
        if order.delivery_status != 'Dispatched':
            for item in order.order_items.all():
                product = item.product
                if product.instock >= item.quantity:
                    product.instock -= item.quantity
                    product.save()
                else:
                    return HttpResponse(f'''<script>alert("Not enough stock for {product.name}."); window.location="/view_orders/";</script>''')

            # Update the delivery status
            order.delivery_status = 'Dispatched'
            order.save()

            # Assign delivery boy for each order item
            try:
                delivery_details = DeliveryDetails.objects.get(checkout=order)
                delivery_boy = DeliveryBoy.objects.filter(pincode=delivery_details.pincode).first()

                if delivery_boy:
                    for order_item in order.order_items.all():
                        OrderAssignDeliveryBoy.objects.create(
                            order=order_item,  # Assigning the correct OrderItem object
                            dboy=delivery_boy,
                            date=now()
                        )
                    message = f"Order dispatched successfully and assigned to {delivery_boy.name}."
                else:
                    message = "Order dispatched successfully, but no delivery boy is available for the pincode."
            except DeliveryDetails.DoesNotExist:
                message = "Order dispatched successfully, but delivery details are missing."
        else:
            message = 'Order has already been dispatched.'
    elif action == 'transit':
        if order.delivery_status == 'Dispatched':
            order.delivery_status = 'In Transit'
            order.save()
            message = 'Order is now in transit.'
        else:
            message = 'Dispatch the order first.'
    elif action == 'delivered':
        if order.delivery_status == 'In Transit':
            if order.payment_status != 'Completed':
                message = "Payment is pending. Please confirm payment before marking as delivered."
                return HttpResponse(f'''<script>alert("{message}"); window.location="/view_deliveryboy_orders/";</script>''')
            else:
                order.delivery_status = 'Delivered'
                order.delivered_at = now()  # Set the delivered_at field
                order.save()
                message = 'Order delivered successfully!'
                return HttpResponse(f'''<script>alert("{message}"); window.location="/view_deliveryboy_orders/";</script>''')
        else:
            message = 'Order not in transit yet.' 
            return HttpResponse(f'''<script>alert("{message}"); window.location="/view_deliveryboy_orders/";</script>''')           
    else:
        message = 'Invalid action.'

    return HttpResponse(f'''<script>alert("{message}"); window.location="/view_orders/";</script>''')

def tracking(request,id):
    order = get_object_or_404(Checkout, id=id)
    return render(request,"tracking.html",{'order': order})

def return_item(request,id):
    order = get_object_or_404(OrderItem,id=id)
    date = datetime.now()
    address = get_object_or_404(DeliveryDetails, checkout=order.checkout)
    item = ReturnedItems(
        order=order,
        date=date,
        delivery=address,       
    )
    item.save()

    return HttpResponse('''<script>alert("Item submitted for return.");window.location="/orders_history/"</script>''')


def view_returns(request):
    seller = Seller.objects.get(login=request.session['lid'])
    seller_products = Product.objects.filter(seller=seller)
    returned_items = ReturnedItems.objects.filter(order__product__in=seller_products)
    return render(request,"view_returns.html",{'returned_items':returned_items})

# def item_returned(request,id):
#     return_item = get_object_or_404(ReturnedItems,id=id)
#     if return_item.status == 'Return Pending':
#         return_item.status = 'Returned Item Picked Up'
#         return_item.save()
#         return HttpResponse('''<script>alert("Item marked as picked up successfully."); window.location="/view_delivery_boy_returns/";</script>''')
#     elif return_item.status == 'Returned Item Picked Up':
#         return_item.status = 'Item Returned'
#         return_item.save()
#         return HttpResponse('''<script>alert("Item set as returned successfully");window.location="/view_returns/"</script>''')
#     else:
#        return HttpResponse('''<script>alert("Item not picked up yet.");window.location="/view_returns/"</script>''') 

def item_returned(request, id, action):
    return_item = get_object_or_404(ReturnedItems, id=id)
    message = ''

    if action == 'pickup':
        if return_item.status == 'Return Pending':
            return_item.status = 'Returned Item Picked Up'
            return_item.save()
            message = "Item marked as picked up successfully."
            redirect_url = "/view_delivery_boy_returns/"
        else:
            message = "Item already picked up."
            redirect_url = "/view_delivery_boy_returns/"

    elif action == 'return':
        if return_item.status == 'Returned Item Picked Up':
            return_item.status = 'Item Returned'
            return_item.save()
            message = "Item set as returned successfully."
            redirect_url = "/view_returns/"
        else:
            message = "Item not picked up yet."
            redirect_url = "/view_returns/"

    else:
        message = "Invalid action."
        redirect_url = "/"

    return HttpResponse(f'''<script>alert("{message}"); window.location="{redirect_url}";</script>''')


def delivery_feedback(request,id):
    user = Signup.objects.get(login=request.session['lid'])
    checkout = Checkout.objects.get(id=id, user=user)
    order_items = OrderItem.objects.filter(checkout=checkout).prefetch_related('returneditems_set')
    rating = request.POST['rating']
    feedback = request.POST['feedback']
    date = datetime.now()

    if not rating:
        return HttpResponse('''<script>alert("Please provide a rating.");window.history.back();</script>''')
    
    dfb=DeliveryFeedback(
        order=order_items.first(),
        user=user,
        feedback=feedback,
        rating=rating,
        date=date
    )
    dfb.save()
    return HttpResponse('''<script>alert("Feedback posted successfully!.");window.location="/orders_history/"</script>''')



def inventory(request):
    seller = Seller.objects.get(login=request.session['lid'])
    products=Product.objects.filter(seller=seller)
    return render(request,"inventory.html", {'products' : products})

def inventory_post(request,id):
    if request.method == "POST":
        try:
            instock = request.POST['instock']
            product = Product.objects.get(id=id)
            product.instock = int(instock)
            product.save()

            # Return a JSON response to indicate success
            return JsonResponse({"status": "success", "message": "Stock updated successfully!"})
        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product not found!"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method!"})
    
def submit_complaint(request):
    user = Signup.objects.get(login=request.session['lid'])
    # checkout = Checkout.objects.get(id=id, user=user)
    # order_items = OrderItem.objects.filter(checkout=checkout)
    order_id = request.POST['order_id']
    complaint = request.POST['complaint']
    date = datetime.now()

    if not complaint.strip():
        return HttpResponse(
            '''<script>alert("Complaint cannot be empty.");window.location="/orders_history/";</script>'''
        )

    order = OrderItem.objects.get(id=order_id, checkout__user=user)
    complaint = Complaint(
      order=order,
      user=user,
      date=date,
      complaint=complaint
    )
    complaint.save()
    return HttpResponse('''<script>alert("Complaint submitted successfully!.");window.location="/orders_history/"</script>''')

def view_complaints(request):
    seller = Seller.objects.get(login=request.session['lid'])
    complaints = Complaint.objects.filter(
        order__product__seller=seller,  # Filter products sold by the seller
        order__checkout__delivery_status="Delivered"  # Only delivered orders
    ).select_related('order', 'user', 'order__product')

    return render(request, "view_complaints.html", {'complaints': complaints})

def deliveryboy_reg(request):
    return render(request,"deliverboy_reg.html")

def deliveryboy_reg_post(request):
    name = request.POST['name']
    emailorphone = request.POST['emailorphone']
    password = request.POST['password']
    salt=''.join(random.choices(string.ascii_letters,k=7))
    # print(str(salt))
    password=salt+password
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    photo = request.FILES.get('photo',None) # Set photo to None if not uploaded
    place = request.POST['place']
    pincode = request.POST['pincode']
    state = request.POST['state']
    gender = request.POST['gender']
    id_proof = request.FILES['id_proof']
    if DeliveryBoy.objects.filter(emailorphone=emailorphone).exists():
        return HttpResponse('''<script>alert("A Delivery Boy account with the provided email or phone number already exists.");window.location="/seller_reg/"</script>''')
    
    lg=Login(
        emailorphone=emailorphone,
        password=password,
        salt=salt,
        type='DeliveryBoy'
    )
    lg.save()
    dboy=DeliveryBoy(
        name=name,
        emailorphone=emailorphone,
        photo=photo,
        place=place,
        pincode=pincode,
        state=state,
        gender=gender,
        id_proof=id_proof,
        login_id=lg.id
    )
    dboy.save()
    return HttpResponse('''<script>alert("Delivery Boy Registered successfully! Please login to continue.");window.location="/login/"</script>''')

def deliveryboy_reg(request):
    return render(request,"deliveryboy_reg.html")

def deliveryboy_reg_post(request):
    name = request.POST['name']
    emailorphone = request.POST['emailorphone']
    password = request.POST['password']
    salt=''.join(random.choices(string.ascii_letters,k=7))
    # print(str(salt))
    password=salt+password
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    photo = request.FILES.get('photo',None) # Set photo to None if not uploaded
    place = request.POST['place']
    pincode = request.POST['pincode']
    state = request.POST['state']
    gender = request.POST['gender']
    id_proof = request.FILES['id_proof']
    if DeliveryBoy.objects.filter(emailorphone=emailorphone).exists():
        return HttpResponse('''<script>alert("An account with the provided email or phone number already exists.");window.location="/deliveryboy_reg/"</script>''')
    
    lg=Login(
        emailorphone=emailorphone,
        password=password,
        salt=salt,
        type='DeliveryBoy'
    )
    lg.save()
    dboy=DeliveryBoy(
        name=name,
        emailorphone=emailorphone,
        photo=photo,
        place=place,
        pincode=pincode,
        state=state,
        gender=gender,
        id_proof=id_proof,
        login_id=lg.id
    )
    dboy.save()
    return HttpResponse('''<script>alert("Delivery boy Registered successfully! Please login to continue.");window.location="/login/"</script>''')
    

from django.shortcuts import render
from .models import Checkout, DeliveryDetails, ReturnedItems, DeliveryFeedback, DeliveryBoy

def deliveryboy_home(request):
    # Assuming the delivery boy is logged in and their ID is available in the request
    delivery_boy = DeliveryBoy.objects.get(login=request.session['lid'])
    
    # Fetch all deliveries assigned to this delivery boy
    deliveries = Checkout.objects.filter(delivery_status__in=['Dispatched', 'In Transit', 'Delivered'])
    
    # Calculate total, completed, and pending deliveries
    total_deliveries = deliveries.count()
    completed_deliveries = deliveries.filter(delivery_status='Delivered').count()
    pending_deliveries = total_deliveries - completed_deliveries
    
    # Define the delivery fee per delivery (e.g., ₹50 per delivery)
    delivery_fee = 50
    
    # Calculate total earnings
    total_earnings = completed_deliveries * delivery_fee
    
    # Fetch recent deliveries (last 10) and add delivery fee to each delivery
    recent_deliveries = deliveries.order_by('-date')[:10]
    for delivery in recent_deliveries:
        delivery.delivery_fee = delivery_fee  # Add delivery fee to each delivery object
    
    # Prepare data for the template
    context = {
        'total_deliveries': total_deliveries,
        'completed_deliveries': completed_deliveries,
        'pending_deliveries': pending_deliveries,
        'deliveries': recent_deliveries,
        'total_earnings': total_earnings,
        'delivery_fee': delivery_fee,
    }
    
    return render(request, "deliveryboy_home.html", context)

def dboy_profile(request):
    dboy = DeliveryBoy.objects.get(login=request.session['lid'])
    return render(request,"dboy_profile.html",{'profile':dboy})

def dboy_profile_edit(request,id):
    dboy=DeliveryBoy.objects.get(id=id)
    dboy.name=request.POST['name']
    if 'photo' in request.FILES:
        dboy.photo=request.POST['photo']
    dboy.place=request.POST['place']
    dboy.pincode=request.POST['pincode']
    dboy.state=request.POST['state']
    dboy.gender=request.POST['gender']
    dboy.save()
    return HttpResponse('''<script>alert("Profile Updated successfully.");window.location="/dboy_profile/"</script>''')

def dboy_change_password_post(request):
    current_password = request.POST['current_password']
    salt=Login.objects.get(id=request.session['lid']).salt
    current_password=salt+current_password
    current_password = hashlib.md5(current_password.encode('utf-8')).hexdigest()

    log=Login.objects.get(id=request.session['lid'])
    # logpass=Login.objects.get(id=request.session['lid']).password
    logpass=log.password

    if logpass==current_password:
        new_password=request.POST['password']

        # Ensure the new password is not the same as the current password
        new_salt=''.join(random.choices(string.ascii_letters,k=7))
        new_password=new_salt+new_password
        new_password = hashlib.md5(new_password.encode('utf-8')).hexdigest()
        if new_password == logpass:
            return HttpResponse('''<script>alert("New password cannot be the same as the current password! Please try again.");window.location="/dboy_profile/"</script>''')
        
        # Update password and salt
        log.salt=new_salt  
        log.password=new_password
        log.save()
        
        return HttpResponse('''<script>alert("Password changed successfully.");window.location="/dboy_profile/"</script>''')
    else:
        return HttpResponse('''<script>alert("Current password incorrect! Please try again.");window.location="/dboy_profile/"</script>''')

def view_deliveryboy_orders(request):
    # Get the logged-in delivery boy
    dboy = DeliveryBoy.objects.get(login=request.session['lid'])
    
    # Fetch unique orders (based on Checkout) assigned to this delivery boy
    assigned_orders = (
        OrderAssignDeliveryBoy.objects.filter(dboy=dboy)
        .select_related('order__checkout')  # Fetch related Checkout object
        .values_list('order__checkout', flat=True)  # Get only the Checkout IDs
        .distinct()  # Remove duplicates
    )
    
    # Prepare order details
    order_details = []
    for checkout_id in assigned_orders:
        checkout = Checkout.objects.get(id=checkout_id)  # Fetch the Checkout instance
        delivery_details = DeliveryDetails.objects.get(checkout=checkout)  # Get delivery details
        
        order_details.append({
            'order': checkout,  # Pass the Checkout instance
            'delivery_details': delivery_details,
            'payment_method': delivery_details.payment_method,
        })
    
    return render(request, 'view_deliveryboy_orders.html', {
        'order_details': order_details,
    })

def cod_payment_received(request, id):
    try:
        order = Checkout.objects.get(id=id)
        if order.payment_status != 'Completed':
            order.payment_status = 'Completed'
            order.save()
            message = "Payment marked as completed."
        else:
            message = "Payment is already marked as completed."
    except Checkout.DoesNotExist:
        message = "Order not found."
    return HttpResponse(f'''<script>alert("{message}"); window.location="/view_deliveryboy_orders/";</script>''')

def view_deliveryboy_order_details(request, id):
    # Ensure the logged-in user is a delivery boy
    dboy = get_object_or_404(DeliveryBoy, login=request.session['lid'])
    
    # Fetch the specific order (Checkout) by its ID
    order = get_object_or_404(Checkout, id=id)
    
    # Verify the order is assigned to this delivery boy
    is_assigned = OrderAssignDeliveryBoy.objects.filter(dboy=dboy, order__checkout=order).exists()
    if not is_assigned:
        return HttpResponseForbidden("You do not have access to this order.")

    # Fetch order items and delivery details for the selected order
    order_items = OrderItem.objects.filter(checkout=order)  # All items in this order
    delivery_details = DeliveryDetails.objects.get(checkout=order)
    
    return render(request, "view_deliveryboy_order_details.html", {
        'order': order,
        'order_items': order_items,
        'delivery_details': delivery_details,
        'date': order.date,
        'payment_status': order.payment_status,
        'delivery_status': order.delivery_status,
        'order_total': order.total,
    })


def view_delivery_boy_returns(request):
    dboy = DeliveryBoy.objects.get(login=request.session['lid'])
    assigned_order_items = OrderAssignDeliveryBoy.objects.filter(dboy=dboy).values_list('order', flat=True)
    returned_items = ReturnedItems.objects.filter(
        order__in=assigned_order_items  # Only consider returned items from orders assigned to the delivery boy
    )
    return render(request,"view_delivery_boy_returns.html",{'returned_items': returned_items})

def view_delivery_feedbacks(request):
    dboy = DeliveryBoy.objects.get(login=request.session['lid'])
    assigned_orders = OrderAssignDeliveryBoy.objects.filter(dboy=dboy)
    feedbacks = DeliveryFeedback.objects.filter(order__in=[assign.order for assign in assigned_orders])
    return render(request,"view_delivery_feedbacks.html", {'feedbacks':feedbacks})

def contact(request):
    user = Login.objects.get(id=request.session['lid'])
    search_history = []
    if user:
        search_history = SearchHistory.objects.filter(user=user).order_by('-searched_at')[:10]
    return render(request,"contact.html",{'user': user, 'search_history':search_history})

def contact_post(request,id):
    user = Login.objects.get(id=request.session['lid'])
    subject = request.POST.get("subject", "").strip()
    message = request.POST.get("message", "").strip()
    date = datetime.now()
    
    if not all([subject, message]):
        return JsonResponse({"success": False, "error": "All fields are required!"})
    
    contact = Contact(
        login=user,
        subject=subject,
        message =message,
        date = date
    )
    contact.save()

    if user.type == "Seller":
        return HttpResponse('''<script>alert("Message sent successfully.");window.location="/contact_for_seller/"</script>''')
    elif user.type == "DeliveryBoy":
        return HttpResponse('''<script>alert("Message sent successfully.");window.location="/contact_for_dboy/"</script>''')
    else:  # Default to customer page
        return HttpResponse('''<script>alert("Message sent successfully.");window.location="/contact/"</script>''')

def contact_for_seller(request):
    return render(request,"contact_for_seller.html")

def contact_for_dboy(request):
    return render(request,"contact_for_dboy.html")


def blog(request):
    return render(request,"blog.html")

def single_blog(request):
    return render(request,"single-blog.html")

def elements(request):
    return render(request,"elements.html")

