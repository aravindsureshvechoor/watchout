from django.shortcuts import render,redirect
from .models import *
from offerapp.models import Coupon,CategoryOffer
from siteadmin.models import *
from cartapp.models import *
from django.contrib import messages,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from decimal import Decimal
import random 
import string


def home(request):

    products = Product.objects.all().filter(is_available=True)
    pros = Product.objects.all()[:8]
    
    context = {
        'products':products,
        'pros':pros,

    }
    return render(request,'usertemplates/index.html',context)


def contact(request):
    return render(request,'usertemplates/contact.html')
    

def generate_unique_referral_id(length=8):
    # Define the set of characters to choose from (alphanumeric)
    characters = string.ascii_letters + string.digits
    # Generate a random ID until a unique one is found
    while True:
        referral_id = ''.join(random.choice(characters) for _ in range(length))
        # Check if the generated referral ID is unique (e.g., by querying your database)
        # If it's unique, return it; otherwise, generate a new one
        if not Referalid.objects.filter(referalid=referral_id).exists():
            return referral_id


def usersignup(request):

    if request.method == "POST":

        first_name   = request.POST['firstname']
        last_name    = request.POST['lastname']
        user_name    = request.POST['username']
        email        = request.POST['email']
        pass1        = request.POST['pass1']
        pass2        = request.POST['pass2']
        referalid    = request.POST['referalid']
        
        if pass1 != pass2:

            messages.success(request,'Passwords does not match')
           
            return redirect('usersignup')

        if Account.objects.filter(user_name = user_name).exists():
            messages.success(request,'User Already Exists')
            
            return redirect('usersignup')
        
        myuser = Account.objects.create_user(first_name=first_name,last_name=last_name,user_name=user_name,email=email,password=pass1)
        myuser.is_active = False
        myuser.is_admin = False
        myuser.is_superuser = False
        myuser.is_staff = False
       
        myuser.save()

        wallet=Wallet.objects.create(currentuser=myuser,amount=0)

        if referalid:
            if Referalid.objects.filter(referalid=referalid).exists():
                ref = Referalid.objects.get(referalid=referalid)
                walletofuser1 = Wallet.objects.get(currentuser=ref.currentuser)
                walletofuser1.amount += 50
                walletofuser1.save()
                wallet.amount += 50
                wallet.save()
            else:
                messages.error(request,'This referal id is not valid')
                    
        Referalid.objects.create(
            referalid=generate_unique_referral_id(),
            currentuser=myuser
        )

        randomotp = str(random.randint(1000, 9999))
        request.session['storedotp'] = randomotp
        request.session.modified = True 
        request.session.set_expiry(300)

        subject = "OTP"
        sendermail = "Watchout Ecommerce Store"
        otp = f"{randomotp}"
        send_mail(subject,otp,sendermail,[email])
        
        context = {
            'email':email
        }
        # messages.success(request,'Your Account Has Been Successfully Created')
        return render(request,'usertemplates/otp.html',context)

    return render(request,'usertemplates/signuptemplate.html')


def otp(request):
    if request.method == "POST":
        otp = request.POST.get('enteredotp')
        email = request.POST.get('email')
        storedotp=request.session['storedotp']

        if otp == storedotp:
            user = Account.objects.get(email=email)
            user.is_active = True
            user.save()
            messages.success(request,'User is Successfully Registered')
            return redirect ('usersignin')
        else:
            messages.error(request,'Wrong Entry')

            context = {
                'email':email
            }
            return render(request,'usertemplates/otp.html',context)
        

    

    return render(request,'usertemplates/otp.html')


def usersignin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email = email , password = password)

        
        if user is not None and user.is_admin == False and user.is_blocked == False:
         
            auth.login(request, user)
            messages.success(request,'Successfuly Logged in')
            return redirect('home')
        
        elif user is not None and user.is_blocked == True:
            messages.error(request,' 0_0ps You are Blocked!')
            return redirect('usersignin')

        else:
            
            messages.error(request,'Bad Credentials!')
            return redirect('usersignin')
        
    return render(request,'usertemplates/signintemplate.html')

def signout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return redirect('home')



def shop(request):
    category = request.GET.get('category')
    if category:
        cat = Category.objects.get(slug=category)
        products = Product.objects.filter(category=cat)
    else:
        products = Product.objects.all()

    items_per_page = 6 
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'products': page, 
    }

    return render(request,'usertemplates/shop.html',context)



def productsorting(request):

    sorting_option=request.GET.get('sorting_option')
    category=request.GET.get('category')
    if category :
        cat = Category.objects.get(slug=category)
   
    if sorting_option == 'lowToHigh':
        products = Product.objects.filter(category=cat).order_by('price')
    elif sorting_option == 'highToLow':
        products = Product.objects.filter(category=cat).order_by('-price')
    
    else:
         products = Product.objects.all()
    items_per_page = 6 
    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'products': page, 
    }

    return render(request,'usertemplates/shop.html',context)


def productinfo(request,product_id):
    products = Product.objects.get(id=product_id)

    
    # try:
    #     offer = CategoryOffer.objects.get(category=products.category)
    #     if offer:
    #         products.offerprice = round(products.price - (products.price / Decimal('100')) * offer.discount_percentage,2)
    #         products.save()
    # except:
    #     pass
    feedbacks = Feedback.objects.filter(product=products).order_by('-created_at')
    items_per_page = 5  
    paginator = Paginator(feedbacks, items_per_page)
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number)

    context = {
        'feedbacks': page,  
        'products': products
    }
    return render(request,'usertemplates/productinfo.html',context)

def accountinfo(request):
    currentuser = request.user
    usr = Account.objects.get(email=currentuser)
    context = {
        'usr':usr
    }
    return render(request,'usertemplates/accountinfo.html',context)

def profilepic(request):
    
    image = request.FILES['product_image']
    currentuser = Account.objects.get(email=request.user)
    currentuser.profilepic = image
    currentuser.save()
    return redirect('accountinfo')

def editaccountinfo(request):

    currentuser = request.user
    usr = Account.objects.get(email=currentuser)
    context = {
        'usr':usr
    }

    return render(request,'usertemplates/editaccountinfo.html',context)

def saveuseredit(request):
     if request.method ==  "POST":

        firstname        = request.POST['first_name']
        lastname         = request.POST['last_name']
        username         = request.POST['user_name']
        email            = request.POST['email']
        
      
        userid          = request.POST['user_id']

        usr = Account.objects.get(id=userid)

        usr.first_name = firstname
        usr.last_name  = lastname
        usr.user_name  = username
        usr.email      = email
        usr.save()
        messages.success(request,'Successfully Saved Changes')

        return redirect('accountinfo')

     return render(request,'usertemplates/editaccountinfo.html')

def discarduseredit(request):
    return redirect('accountinfo')

def addaddress(request):
    return render(request,'usertemplates/addaddress.html')

def submitaddress(request):
    if request.method == 'POST':
        currentuser = Account.objects.get(id=request.user.id)
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        homeaddress = request.POST['homeaddress']
        city = request.POST['city']
        pincode = request.POST['pincode']

        address = UserAddress.objects.create(
            currentuser = currentuser,
            firstname   = firstname,
            lastname    = lastname,
            email       = email,
            phone       = phone,
            homeaddress = homeaddress,
            city        = city,
            pincode     = pincode
            )
        address.save()
        messages.success(request,'Address successfully added')

    return redirect('addaddress')

def ordertimesubmitaddress(request):
    if request.method == 'POST':
        currentuser = Account.objects.get(id=request.user.id)
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        homeaddress = request.POST['homeaddress']
        city = request.POST['city']
        pincode = request.POST['pincode']

        address = UserAddress.objects.create(
            currentuser = currentuser,
            firstname   = firstname,
            lastname    = lastname,
            email       = email,
            phone       = phone,
            homeaddress = homeaddress,
            city        = city,
            pincode     = pincode
            )
        address.save()
        messages.success(request,'Address successfully added')

    return redirect('checkout')

def editaddress(request):

    addresses = UserAddress.objects.filter(currentuser=request.user)

    context = {

        'addresses':addresses
    }
    return render(request,'usertemplates/editaddress.html',context)

def editaddressview(request):
    addressid = request.GET.get('address_id')
    address = UserAddress.objects.get(id=addressid)

    context = {
        'address':address
    }

    return render(request,'usertemplates/editaddressview.html',context)

def addresssave(request):
    addressid = request.POST['address_id']
    address = UserAddress.objects.get(id=addressid)

    address.firstname = request.POST['firstname']
    address.lastname = request.POST['lastname']
    address.email = request.POST['email']
    address.phone = request.POST['phone']
    address.homeaddress = request.POST['homeaddress']
    address.city = request.POST['city']
    address.pincode = request.POST['pincode']

    address.save()
    messages.success(request,'Changes have been made')

    return redirect('editaddress')



#thisfunction 'discard' is for the discard button next to the save button 
def discard(request):
    return redirect('editaddress')

def addressdelete(request):

    addressid = request.GET.get('adrs_id')
    address = UserAddress.objects.get(id=addressid)
    address.delete()
    messages.success(request,'Address removed')


    return redirect('editaddress')



def addfeedback(request,product_id):
    try:
        if request.user.is_authenticated:
            if request.method == "POST":
                currentuser = request.user
                product =  Product.objects.get(id=product_id)
                comment = request.POST['comment']

                Feedback.objects.create(currentuser=currentuser,product=product,comment=comment)
        return redirect('feedback',product_id=product_id)
    except:
        messages.error(request,'Sign in to post a feedback')
        return redirect('feedback')

def feedback(request,product_id):
    products = Product.objects.get(id=product_id)
    feedbacks = Feedback.objects.filter(product=products).order_by('-created_at')
    items_per_page = 5  
    paginator = Paginator(feedbacks, items_per_page)
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number)

    context = {
        'feedbacks': page,  
        'products': products
    }

    return render(request, 'usertemplates/feedback.html', context)

def coupondetails(request):
    coupons = Coupon.objects.all()
    context = {
        'coupons':coupons
    }
    return render(request,'usertemplates/offer.html',context)

def search(request):
    products = Product.objects.all()
    if request.method=="POST":
        search_query = request.POST['search_query']
        products = products.filter(product_name__icontains=search_query)


    context = {
        'products':products
    }
    return render(request,'usertemplates/search_query.html',context)
        
def invoice(request,order_id):

    orders = Order.objects.get(id=order_id)
    total = orders.order_total+orders.tax
    grand_total = round(total-float(orders.discount_price),2)
    discount_price=orders.discount_price
    context = {
        'orders':orders,
        'grand_total':grand_total,
        'discount_price':discount_price
    }
    return render(request,'usertemplates/invoicedownload.html',context)

def wallet(request):
    wallet = Wallet.objects.get(currentuser=request.user)
    c_user = Account.objects.get(email=request.user)
    ref    = Referalid.objects.get(currentuser=request.user)

    context = {
        'wallet':wallet,
        'c_user':c_user,
        'ref'   :ref
    }
    return render(request,'usertemplates/wallet.html',context)