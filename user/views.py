from django.shortcuts import render, redirect,get_object_or_404
from adminapp.models import Product
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control, never_cache
import re
from adminapp import views
from adminapp .models import Banner
from django.contrib import messages
from django.db.models import Q
from adminapp.models import Product, Color,Size
from.models import UserProfile,AddressUS, Wallet
from core.models import ProductOrder,Order
from django.db.models import Sum
from adminapp.models import Category
from django.utils import timezone
from adminapp.models import *

import random
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.db import transaction

from django.contrib.auth import update_session_auth_hash
from django.db.models import Q






@never_cache
def home(request):
    if request.user.is_anonymous:
        return redirect('login_view')

    products = Product.objects.filter(is_active=True)
    category_list = Category.objects.all()
    all_offers=Offer.objects.all()
    applied_offer=Offer.objects.all()
    banners = Banner.objects.filter(is_active=True)
    search_query=request.GET.get('search','')
    if search_query:

        products = products.filter(
            Q(product_name__icontains=search_query) |
            Q(product_description__icontains=search_query)
        )

    # Calculate days difference for each banner
    for banner in banners:
        banner.days_difference = (timezone.now() - banner.created_at).days
        print(f"Banner ID: {banner.id}, Created At: {banner.created_at}, Days Difference: {banner.days_difference}")
    
        

    if not request.user.is_active:
        request.session.flush()
        print(applied_offer)

    

    context = {
        'products': products,
        'category': category_list,
        'banners': banners,
        'search_query': search_query,
        'all_offers': all_offers,
        'applied_offer': applied_offer,
    }
    print("Applied Offer:", applied_offer)
    for product in products:
        print(f"Product: {product.product_name}, Offer: {applied_offer}")

    return render(request, 'accounts/home.html', {'username': request.user.username, **context})

    

@never_cache
def login_view(request):
    if 'username' in request.session:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if not username or not password:
            error = "Both username and password are required."
            return render(request, 'accounts/login_view.html', {'error': error})

        user=authenticate(username=username,password=password)
        if user is not None:
            request.session['username']=username
            login(request,user)
            return redirect("home")
        else:
            error = "Invalid credentials"
            return render(request, 'accounts/login_view.html', {'error': error})

    return render(request,'accounts/login_view.html')# Assuming you have a URL named 'login'

@cache_control(must_revalidate=True, no_transform=True, no_cache=True, no_store=True)
def signup_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('pass1')
        confrim_password=request.POST.get('pass2')

        request.session['uname'] = username
        request.session['email'] = email
        request.session['password'] = password



        try:
            if not username or  not email or not password:
                messages.error(request, 'Enter details to field')
                return redirect('signup_view')
        except:
            pass

        try:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different one.")
                return redirect("signup_view")
            elif not username.isalnum():
                messages.warning(request, "Username contains invalid characters. Please use only letters and numbers.")
                return redirect("signup_view")
        except:
            pass

        try:
            if User.objects.filter(email=email):
                messages.error(request, "Email already exists")
                return redirect("signup_view")
        except:
            pass

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address")
            return redirect('signup_view')

        try:
            if password !=confrim_password:
                messages.error(request, "passwords not matching")
                return redirect("signup_view")
        except:
            pass

        try:
            if len(username)>20:
                messages.error(request, "username is too long")
                return redirect("signup_view")
        except:
            pass

        try:
            if len(password)<8:
                messages.error(request, "Password must be at least 8 characters")
                return redirect("signup_view")
        except:
            pass

        request.session['verification_type'] = 'signup_view'
        send_otp(request)
        return render(request, 'accounts/otp_verification.html')

    return render(request, 'accounts/signup_view.html')
import time
from datetime import datetime

def send_otp(request):
    s=""
    for x in range(0,4):
        s+=str(random.randint(0,9))
    print(s)
    request.session["otp"] = s
    request.session["otp_creation_time"] = time.time()
    
    
    email = request.session.get('email')
    send_mail("otp for sign up", s, 'bisherp2@gmail.com', [request.session['email']], fail_silently=False)
    return render(request, 'accounts/otp_verification.html')
   

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

# ... (other imports)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
import random
import time
from django.core.mail import send_mail
from django.urls import reverse

def otp_verification(request):
    print("Inside otp_verification view")
    print(f"Session data before redirection: {request.session}")

    email = request.session.get('email', '')  # Define email here with a default value

    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        otp_sent = request.session.get('otp')

        # Get OTP creation time from session
        otp_creation_time = request.session.get('otp_creation_time', 0)

        # Check if OTP is expired (more than 60 seconds old)
        if time.time() - otp_creation_time > 60:
            messages.error(request, "OTP has expired. Please request a new one.")
            return render(request, 'accounts/otp_verification.html', {"email": email})

        user_id = request.session.get('user_id')
        verification_type = request.session.get('verification_type')

        print(f"Verification type: {verification_type}")

        if otp_entered == otp_sent:
            username = request.session.get('uname')
            email = request.session.get('email')
            password = request.session.get('password')

            if verification_type == 'signup_view':
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login_view')  # Redirect to login page for signup_view

            elif verification_type == 'login_view':
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    username = user.username
                    request.session['username'] = username
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid credentials')
                    return redirect('login_view')

        elif verification_type == 'forgot_password':
                new_password = request.POST.get('new_password')  # Retrieve the new password from the form

                try:
                    user = User.objects.get(id=user_id, email=email)
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password updated successfully!')
                    
                    return redirect('forgot_password')  # Redirect to login page for forgot_password

                except User.DoesNotExist:
                    messages.error(request, 'User does not exist.')
                    return redirect('login_view')  # Redirect to login page for forgot_password

                except Exception as e:
                    messages.error(request, f'Error updating password: {e}')

        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, 'accounts/otp_verification.html', {"email": email})

    # Handle GET requests by rendering the OTP verification form
    return render(request, 'accounts/otp_verification.html', {"email": request.session.get('email')})



def resend_otp(request):
    new_otp = "".join([str(random.randint(0, 9)) for _ in range(4)])
    print("New OTP:", new_otp)
    email = request.session.get('email')
    send_mail("New OTP for Sign Up", new_otp, 'bisherp2@gmail.com', [email], fail_silently=False)
    request.session['otp'] = new_otp
    print("Resending OTP...")

# ... (other views)



def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login_view') 



def product_list(request):
    products = Product.objects.all()
    print(products)

    return render(request, 'admin/product_list.html', {'products': products})

def category_list(request):
    category_list = Category.objects.all()
    print(category_list)
    return render(request, 'admin/admin_category.html', {'category_list': category_list})

def product_detials(request, product_id):
    product = Product.objects.get(pk=product_id)
    size_options = Size.objects.filter(is_active=True)
    color_options = Color.objects.filter(is_active=True)
    context = {'color_options': color_options, 'size_options': size_options, 'product': product}
    
    return render(request, 'accounts/product_detials.html', {'product': product,**context})



 # Import the Color and Size models from the admin app

def size_color_options(request):
    size_options = Size.objects.filter(is_active=True)
    color_options = Color.objects.filter(is_active=True)
    context = {'size_options': size_options, 'color_options': color_options}
    return render(request, 'product_list.html',context)





@login_required
def view_profile(request):
    try:
        # Assuming the user profile is related to the logged-in user
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        # If the profile does not exist, you can handle it here.
        # For example, you can redirect to a profile creation page or show an error message.
        # For simplicity, setting user_profile to None in this case.
        user_profile = None

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required
def change_image_view(request):
    try:
        # Assuming the user profile is related to the logged-in user
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        # If the profile does not exist, create a new one
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST' and 'new_image' in request.FILES:
        new_image = request.FILES['new_image']
        user_profile.image = new_image
        user_profile.save()
        return redirect('view_profile')  # Redirect to the profile view after changing the image

    return render(request, 'accounts/dashboard.html', {'user_profile': user_profile})

@login_required
def add_address(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address_1 = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        try:
            new_address = AddressUS.objects.create(
                first_name=first_name,
                last_name=last_name,
                address_1=address_1,
                city=city,
                state=state,
                zipcode=zip_code,
                user_profile=request.user.profile  # Use 'user_profile' to link to the UserProfile
            )

            # Check if the user has any addresses and set the first one as default if none is set
            user_addresses = AddressUS.objects.filter(user_profile=request.user.profile)
            if not any(address.is_default for address in user_addresses):
                first_address = user_addresses.first()
                if first_address:
                    with transaction.atomic():
                        first_address.is_default = True
                        first_address.save()

            messages.success(request, 'Address added successfully.')
            return redirect('view_profile')  # Redirect to an appropriate page

        except Exception as e:
            print(f"Error creating or updating address: {e}")
            messages.error(request, 'Error adding address. Please try again.')

    return render(request, 'accounts/add_address.html')



@login_required
def addresses(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    addresses = AddressUS.objects.filter(user_profile=user_profile)

    # Check if there is no default address set, and set the first address as default
    if not any(address.is_default for address in addresses):
        first_address = addresses.first()
        if first_address:
            with transaction.atomic():
                first_address.is_default = True
                first_address.save()

    return render(request, 'accounts/address.html', {'addresses': addresses})

def set_default_address(request, address_id):
    address = get_object_or_404(AddressUS, id=address_id)
    address.is_default = True

    # Unset the "is_default" field for other addresses
    AddressUS.objects.filter(user_profile=address.user_profile).exclude(id=address_id).update(is_default=False)

    # Corrected redirect statement
    return redirect('addresses')



def order_list(request):
    # Assuming you want to fetch all orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }

    return render(request, 'accounts/order_list.html', context)


def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_products = ProductOrder.objects.filter(order=order)

    context = {
        'order': order,
        'order_products': order_products,
        
    }

    return render(request, 'accounts/order_view.html',context)


def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Debugging statement to print order status before update
    print(f"Order Status Before Update: {order.status}")

    # Implement your cancel logic here
    # For example, update the order status to 'Cancelled'
    order.status = 'Cancelled'
    order.save()

    # Debugging statement to print order status after update
    print(f"Order Status After Update: {order.status}")

    # Optionally, perform other cancellation actions

    # Redirect to the order list page
    return redirect('order_list')

def return_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = "Returned"
    order.save()

    # Redirect to the reason_view for the given order_id
    return redirect('order_list')

    # Handle the case where the order status is not "Returned"
   

def add_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Add the product to the wishlist
    user_profile.wishlist.add(product)

    return redirect('home')


def wishlist_view(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the user's profile and wishlist items
        user_profile = UserProfile.objects.get(user=request.user)
        wishlist_items = user_profile.wishlist.all()

        # Render the wishlist template with the wishlist items
        return render(request, 'accounts/wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return redirect('home')
    

def delete_wishlist_item(request, product_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    wishlist_item = get_object_or_404(user_profile.wishlist, pk=product_id)

    # Check if the wishlist item belongs to the current user
    if request.user == user_profile.user:
        # Remove the product from the wishlist
        user_profile.wishlist.remove(wishlist_item)
        messages.success(request, "Item removed from wishlist.")
        return redirect('wishlist')
    else:
        messages.error(request, "Wishlist item does not belong to the current user.")
        return redirect('home')
from decimal import Decimal

# ...
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


# views.py
from django.shortcuts import render
from django.db.models import Sum, DecimalField
from django.http import HttpResponseServerError
from decimal import Decimal


def wallet(request):
    # Fetch the list of orders for the user
    order_list = Order.objects.filter(user=request.user).order_by('-created_at')

    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Try to get the user's wallet or create one if it doesn't exist
    user_wallet, created = Wallet.objects.get_or_create(user_profile=user_profile)

    # Check if the updated wallet balance is present in the session
    updated_wallet_balance = request.session.get('updated_wallet_balance', None)

    # Initialize total_returned_amount and total_canceled_amount
    total_returned_amount = Decimal('0.00')
    total_canceled_amount = Decimal('0.00')

    if updated_wallet_balance is not None:
        # If present, use the value from the session
        user_wallet.balance = Decimal(updated_wallet_balance)
        user_wallet.save()

        # Remove 'updated_wallet_balance' from the session
        # del request.session['updated_wallet_balance']
        # request.session.save()
        
        

    else:
        # Otherwise, calculate the total amount of returned and canceled orders
        total_returned_amount = Order.objects.filter(user=request.user, status="Returned").aggregate(Sum('order_total'))['order_total__sum'] or Decimal('0.00')
        total_canceled_amount = Order.objects.filter(user=request.user, status="Cancelled").aggregate(Sum('order_total'))['order_total__sum'] or Decimal('0.00')
        user_wallet.balance = total_returned_amount + total_canceled_amount
        user_wallet.save()
        

        # Update the wallet balance by setting it to the sum of returned and canceled amounts
        request.session['user_wallet.balance'] = str(user_wallet.balance)
        request.session.save()
        updated_wallet_balance = request.session['user_wallet.balance']
        print(updated_wallet_balance)


    # Fetch the latest wallet balance from the database
    user_wallet.refresh_from_db()

    # Print statements for debugging
    print(f'User ID: {request.user.id}')
    print(f'Wallet Balance (from database): {user_wallet.balance}')
    print(f'Updated Wallet Balance (from session): {updated_wallet_balance}')
    print(f'Total Returned Amount: {total_returned_amount}')
    print(f'Total Canceled Amount: {total_canceled_amount}')

    # Prepare the context for rendering
    context = {
        'user_wallet': user_wallet,
        'order_list': order_list,
        'total_returned_amount': total_returned_amount,
        'total_canceled_amount': total_canceled_amount,
        'updated_wallet_balance': str(user_wallet.balance)
        
    }
    # request.session.pop('updated_wallet_balance', None)
    # print(('updated_wallet_balance', None))

    return render(request, 'accounts/wallet.html', context)

 
# def reason_view(request, order_id):
#     # Implement logic for the reason_view here
#     # This could include rendering a template for the user to provide the return reason
#     # or any other logic you need

#     context = {'order_id': order_id}
    
#     # Render the reason template with the context
#     return render(request,'accounts/reason_view.html', context)




def email_valid(request):
    if request.method == 'POST':
        provided_email = request.POST.get('email')
        print(f"Provided Email: {provided_email}")

        try:
            validate_email(provided_email)
            users = User.objects.filter(email=provided_email)

            if users.exists():
                if users.count() == 1:
                    user = users.first()

                    # Store user and email in session for verification in otp_verification view
                    request.session['user_id'] = user.id
                    request.session['email'] = provided_email
                    request.session['verification_type'] = 'forgot_password'  # Set the correct verification_type for forgot password

                    # Call send_otp function from your utils module
                    send_otp(request)

                    print("Redirecting to otp_verification")
                    return redirect('otp_verification')

                else:
                    messages.error(request, 'Multiple users with the same email. Contact support.')
                    print("Redirect failed: Multiple users")
                    return render(request, 'accounts/email_valid.html')

            else:
                messages.error(request, 'User with this email does not exist.')
                print("Redirect failed: User does not exist")
                return render(request, 'accounts/email_valid.html')

        except ValidationError as e:
            print(f"Email validation error: {e}")
            messages.error(request, 'Invalid email address.')
            print("Redirect failed: Invalid email address")
            return render(request, 'accounts/email_valid.html')

        except Exception as e:
            print(f"Error sending OTP: {e}")
            messages.error(request, 'Error sending OTP. Please try again.')
            print("Redirect failed: Error sending OTP")
            return render(request, 'accounts/email_valid.html')

    # If the request method is GET, handle it here
    return render(request, 'accounts/email_valid.html')


def forgot_password(request):
    if request.method == 'POST':
        # Get user details from session
        user_id = request.session.get('user_id')
        email = request.session.get('email')

        try:
            # Update the user's password
            user = User.objects.get(id=user_id, email=email)

            # Retrieve the new password and confirmation password from the form
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # Validate that the new password matches the confirmation password
            if new_password != confirm_password:
                messages.error(request, 'New password and confirmation password do not match.')
                return redirect('forgot_password')

            # Validate the new password
            if len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return redirect('forgot_password')

            # Update the user's password
            user.set_password(new_password)
            user.save()

            # Clear only the specific session data related to password reset
            

            # Redirect to the login page
            messages.success(request, 'Password updated successfully!')
            return redirect('login_view')

        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('login_view')

        except Exception as e:
            messages.error(request, f'Error updating password: {e}')

    return render(request, 'accounts/forgot_password.html')

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def shop_lists(request):
    products = Product.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    categories = Category.objects.filter(is_blocked=True)

    min_price = float(request.GET.get('min_price', 0))

    max_price_param = request.GET.get('max_price')
    if max_price_param is not None:
        max_price = float(max_price_param)
    else:
        # Use a large number instead of infinity
        max_price = 1e20

    # Filter products based on the offer price range
    filtered_products = Product.objects.filter(offer_price__gte=min_price, offer_price__lte=max_price)
    # selected_brand =request.GET.get('brand')
    # selected_category= request.GET.get('caategory')

    # if selected_category:
    #     products = products.filter(category__category_name=selected_category)
    # if selected_brand:
    #     products = products.filter(brand__brand_name=selected_brand)

     # Pagination logic
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 12)  # Show 12 products per page
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    



    context = {
        "products": filtered_products,
        "brands": brands,
        'categories': categories,
        
    }

    return render(request, 'accounts/shop.html', context)


def filter_products_by_category(request, category_name):
    # Filter products based on the selected category
    category_products = Product.objects.filter(category__category_name=category_name, is_active=True)

    # Get the selected price range
    min_price = float(request.GET.get('min_price', 0))
    max_price_param = request.GET.get('max_price')

    if max_price_param is not None:
        max_price = float(max_price_param)
    else:
        # Use a large number instead of infinity
        max_price = 1e20

    # Filter products based on the offer price range
    filtered_products = category_products.filter(offer_price__gte=min_price, offer_price__lte=max_price)

    return render(request, 'accounts/shop.html', {'products': filtered_products})


def filter_products_by_brand(request, brand_name):
    # Filter products based on the selected brand
    brand_products = Product.objects.filter(brand__brand_name=brand_name, is_active=True)

    # Get the selected price range
    min_price = float(request.GET.get('min_price', 0))
    max_price_param = request.GET.get('max_price')

    if max_price_param is not None:
        max_price = float(max_price_param)
    else:
        # Use a large number instead of infinity
        max_price = 1e20

    # Filter products based on the offer price range
    filtered_products = brand_products.filter(offer_price__gte=min_price, offer_price__lte=max_price)

    return render(request, 'accounts/shop.html', {'products': filtered_products})