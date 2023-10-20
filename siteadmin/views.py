from django.shortcuts import render,redirect
from ecommerce.models import *
from .models import *
from offerapp.models import Coupon,CategoryOffer
from ecommerce.models import Order
from django.contrib import messages,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.core.paginator import Paginator
from datetime import timedelta, datetime, time, timedelta, date
from decimal import Decimal
from django.db.models.functions import TruncMonth
from django.db.models import Count



def adminsignin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email = email , password = password)

        if user is not None and user.is_admin == True:
            auth.login(request, user)
            messages.success(request,'Successfuly Logged in')

            return redirect('admindashboard')


        else:
            messages.error(request,'Bad Credentials!')
            return render(request,'admintemplates/adminloginpage.html')

    return render(request,'admintemplates/adminloginpage.html')



def adminlogout(request):
    logout(request)
    messages.success(request,'Successfuly Logged Out')
    return redirect('adminhome')



def productmanagement(request):
    return render(request,'admintemplates/prouctmanagement.html')



def usermanagement(request):
    users = Account.objects.all().exclude(is_superuser=True)
    paginator = Paginator(users,10)
    page = request.GET.get('page')
    paged_users = paginator.get_page(page)
    user_count = users.count()
    
    context = {
        'users':paged_users,
        'user_count':user_count
    }
    return render(request,'admintemplates/usermanagement.html',context)



def categorymanagement(request):
    categories = Category.objects.all().order_by('-id')
    paginator = Paginator(categories,10)
    page = request.GET.get('page')
    paged_categories = paginator.get_page(page)
    category_count = categories.count()
    context = {
        'categories':paged_categories,
        'category_count':category_count
    }
    return render(request,'admintemplates/categorymanagement.html',context)



def admindashboard(request):
    users = Account.objects.all().count()
    # products = Product.objects.all().count()
    prods = Product.objects.all()
    p = prods.count()
    productcount = {}
    prodcount = []
    for product in prods:
        count = OrderProduct.objects.filter(product=product).count()
        productcount[product.product_name] = count

    prodcount = list(productcount.values())
    orders = Order.objects.all().count()

    data = Order.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(sales=Count('id'))
    months = []
    totals = []

    for entry in data:
        months.append(entry['month'].strftime("%b %Y"))
        totals.append(entry['sales'])
    
    context = {
            'users':users,
            'prodcount':prodcount,
            'orders':orders,
            'prods':prods,
            'p':p,
            'months':months,
            'totals':totals
            }

    return render(request,'admintemplates/index.html',context)



def addcategory(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        # slug          = request.POST.get('category_slug')
        description   = request.POST.get('category_description')

        category = Category(
            category_name = category_name,
            # slug          = slug,
            description   = description
        )

        category.save()
        return redirect('categorymanagement')
    return render(request,'admintemplates/addcategory.html')



def editcategory(request):

    if request.method ==  "POST":

        categoryname = request.POST['category_name']
        # categoryslug = request.POST['category_slug']
        categorydescription = request.POST['category_description']
        category_id = request.POST['category_id']
        categoryslug = slugify(categoryname)

        categ = Category.objects.get(id=category_id)
        categ.category_name = categoryname
        categ.description = categorydescription
        categ.slug = categoryslug
        categ.save()
        messages.success(request,'Successfully Saved')
        return redirect('categorymanagement')

    else:

        id = request.GET.get('cat_id')

        cats = Category.objects.get(id=id)
        context = {
            'cats':cats
        }
        return render(request,'admintemplates/editcategory.html',context)

def deactivatecategory(request,category_id):
    category = Category.objects.get(id=category_id)
    category.is_available = False
    category.save()
    products = Product.objects.filter(category=category)
    for product in products:
        product.is_available = False
        product.save()

    return redirect('categorymanagement')

def activatecategory(request,category_id):
    category = Category.objects.get(id=category_id)
    category.is_available = True
    category.save()
    products = Product.objects.filter(category=category)
    for product in products:
        product.is_available = True
        product.save()
    return redirect('categorymanagement')


def deletecategory(request):
    id = request.GET.get('c_id')

    deletecat = Category.objects.get(id=id)
    deletecat.delete()
    messages.success(request,'Succesfully Deleted')

    return redirect('categorymanagement')



def addproduct(request):

    if request.method == "POST":
        productname        = request.POST['product_name']
        category_id        = request.POST['category_id']
        productdescription = request.POST['product_description']
        productprice       = request.POST['product_price']
        productstock       = request.POST['product_stock']
        # productslug        = request.POST['product_slug']
        productimage       = request.FILES['product_image']
      

        category = Category.objects.get(id=category_id)
        product = Product(
            product_name = productname,
            category     = category,
            # slug         = productslug,
            description  = productdescription,
            offerprice   = productprice,
            price        = productprice,
            stock        = productstock,
            images       = productimage   
        )

        product.save()


        messages.success(request, 'Product Added.')
        return redirect('productmanagement')

    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request,'admintemplates/addproduct.html',context)

def discardcategorychanges(request):
    return redirect('categorymanagement')


def productmanagement(request):
    products = Product.objects.all().order_by('-id')
    paginator = Paginator(products,3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()
    

    context = {
        'products':paged_products,
        'product_count':product_count
    }

    return render(request,'admintemplates/prouctmanagement.html',context)




def deleteproduct(request):
    id = request.GET.get('id')
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('productmanagement')

def deactivateproduct(request,product_id):
    product = Product.objects.get(id=product_id)
    product.is_available = False
    product.save()
    return redirect('productmanagement')

def activateproduct(request,product_id):
    product = Product.objects.get(id=product_id)
    product.is_available = True
    product.save()
    return redirect('productmanagement')


def editproduct(request):
    
    if request.method ==  "POST":

        productname        = request.POST['product_name']
        productslug        = slugify(productname)
        productdescription = request.POST['description']
        productprice       = request.POST['price']
        productstock       = request.POST['stock']
        productimages      = request.FILES.get('images')
        productcategory    = request.POST['category_id']
        productid          = request.POST['product_id']

        category = Category.objects.get(id=productcategory)

        product              = Product.objects.get(id=productid)
        product.product_name = productname
        product.slug         = productslug
        product.description  = productdescription
        product.stock        = productstock
        product.category     = category
        product.price        = productprice
        product.offerprice   = productprice

        if productimages is not None:
            product.images = productimages
        product.save()
        messages.success(request,'Successfully Saved')
        return redirect('productmanagement')

    
    category = Category.objects.all()
    id = request.GET.get('p_id')

    pros = Product.objects.get(id=id)
    context = {
        'pros':pros,
        'category':category,
    }

    return render(request,'admintemplates/editproduct.html',context)

def discardproductchanges(request):
    return redirect('productmanagement')


def blockuser(request):
    id = request.GET.get('user_id')

    user = Account.objects.get(id=id)
    if request.user.is_authenticated and request.user == user:
        logout(request)
        request.session.flush()
    user.is_blocked = True
    user.save()
    messages.success(request,'User is Successfully Blocked')
    return redirect('usermanagement')
    
def unblockuser(request):
    id = request.GET.get('usr_id')

    user =  Account.objects.get(id=id)
    user.is_blocked = False
    user.save()
    messages.success(request,'User is unblocked ')
    return redirect('usermanagement')

def deleteuser(request):
    id = request.GET.get('user_id')

    user = Account.objects.get(id=id)
    user.delete()
    messages.success(request,'User is Successfully Deleted')
    return redirect('usermanagement')
    

def ordermanagement(request):
    orders = Order.objects.all().order_by('-created_at')
    paginator = Paginator(orders, 10)  # Change 10 to the number of items per page you want

    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)

    context = {
        'orders': paged_orders,
    }

    return render(request, 'admintemplates/ordermanagement.html', context)

def admin_change_order_status(request,order_id):
    order = Order.objects.get(id=order_id)
    status = request.POST.get(f'status-{order_id}')
    order.status = status
    order.save()
    context ={
        "status":status
    }
    return redirect('ordermanagement')

def coupon(request):
    coupons = Coupon.objects.all()
    paginator = Paginator(coupons, 5) 

    page = request.GET.get('page')
    paged_coupons = paginator.get_page(page)

    context = {
        'coupons': paged_coupons,
    }
    
    return render(request, 'admintemplates/Coupons.html', context)

def addcoupon(request):

    if request.method == "POST":
        enddate = request.POST['expiry_date']
        discount_percentage = request.POST['discount_percentage']

        yr = int(date.today().strftime('%Y'))
        dt = int(date.today().strftime('%d'))
        mt = int(date.today().strftime('%m'))
        d = date(yr,mt,dt)
        cur_date = d.strftime('%Y%m%d')
        

        coupon = Coupon.objects.create(
            enddate=enddate,
            discount_percentage = discount_percentage,
           
        )
        coupon.code =  "CPN"+cur_date+str(coupon.id)
        coupon.save()

        return redirect('coupon')
       

    return render(request,'admintemplates/addcoupon.html')

def editcoupon(request,coupon_id):

    if request.method == "POST":
        code = request.POST['coupon_code']
        discount_percentage = request.POST['discount_percentage']
        startdate = request.POST['validfrom']
        enddate = request.POST['expiry_date']
        cpn = Coupon.objects.get(id=coupon_id)
        cpn.code = code
        cpn.discount_percentage = discount_percentage
        cpn.startdate = startdate
        cpn.enddate = enddate
        cpn.save()
        messages.success(request,'Saved successfully')
        return redirect('coupon')

    coupon = Coupon.objects.get(id=coupon_id)
    context = {
        'coupon':coupon
    }
    return render(request,'admintemplates/editcoupon.html',context)

def discardcouponchanges(request):
    return redirect('coupon')

def deletecoupon(request):
    coupon_id = request.GET.get('id')
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.delete()
    messages.success(request,'Coupon deleted')
    return redirect('coupon')

def categoryoffer(request):
    offers = CategoryOffer.objects.all()
    context = {
        'offers':offers
    }
    return render(request,'admintemplates/categoryoffer.html',context)

def addcategoryoffer(request):
    if request.method == "POST":
        enddate = request.POST['expiry_date']
        discount_percentage = request.POST['discount_percentage']
        category_id = request.POST['category_id']

        category = Category.objects.get(id=category_id)

        CategoryOffer.objects.create(
            enddate=enddate,
            discount_percentage=discount_percentage,
            category=category
        )
    
        # offer = CategoryOffer.objects.filter(category=category)
        products = Product.objects.filter(category=category)

        for product in products:
            product.price = Decimal(product.price)
            discount_percentage = Decimal(discount_percentage)

            # Perform the calculation
            product.offerprice = round(product.price - (product.price / Decimal('100') * discount_percentage), 2)
            product.save()
       
        messages.success(request,'New category offer added')

        return redirect('categoryoffer')

    categories = Category.objects.all()
    context = {
        'categories':categories
    }

    return render(request,'admintemplates/addcategoryoffer.html',context)

def editcategoryoffer(request,category_id):
    cat = Category.objects.get(id=category_id)
    offer = CategoryOffer.objects.get(category=cat)


    if request.method == "POST":
        enddate = request.POST['expiry_date']
        discount_percentage = request.POST['discount_percentage']

        offer.discount_percentage = discount_percentage
        offer.enddate = enddate
        offer.save()

        products = Product.objects.filter(category=cat)

        for product in products:
            product.price = Decimal(product.price)
            discount_percentage = Decimal(discount_percentage)

            # Perform the calculation
            product.offerprice = round(product.price - (product.price / Decimal('100') * discount_percentage), 2)
            product.save()

        return redirect('categoryoffer')




    
    context = {
        'offer':offer
    }
    return render(request,'admintemplates/editcategoryoffer.html',context)

def discardedit(request):
    return redirect('categoryoffer')
    
def deletecategoryoffer(request,category_id):
    cat = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=cat)
    for product in products:
        product.offerprice = product.price
        product.save()
    offer = CategoryOffer.objects.filter(category=cat)
    offer.delete()
    messages.success(request,'Offer deleted')

    return redirect('categoryoffer')

def chart(request):
    users = Account.objects.all().count()
    # products = Product.objects.all().count()
    prods = Product.objects.all()
    p = prods.count()
    productcount = {}
    prodcount = []
    for product in prods:
        count = OrderProduct.objects.filter(product=product).count()
        productcount[product.product_name] = count

    prodcount = list(productcount.values())
    orders = Order.objects.all().count()

    data = Order.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(sales=Count('id'))
    months = []
    totals = []

    for entry in data:
        months.append(entry['month'].strftime("%b %Y"))
        totals.append(entry['sales'])
    
    context = {
            'users':users,
            'prodcount':prodcount,
            'orders':orders,
            'prods':prods,
            'p':p,
            'months':months,
            'totals':totals
            }
    return render(request,'admintemplates/index.html',context)

def reports(request):
    if request.method == "POST":
        startdate = request.POST['start_date']
        enddate = request.POST['end_date']

        start_date = datetime.strptime(startdate, '%Y-%m-%d')
        end_date = datetime.strptime(enddate, '%Y-%m-%d')

        # Filter orders within the specified date range
        orders_page = Order.objects.filter(created_at__range=(start_date, end_date))
        # paginator = Paginator(orders, 10)
        # page = request.GET.get('page')
        # orders_page = paginator.get_page(page)
        context = {
            'orders_page':orders_page
        }
        return render(request,'admintemplates/reports.html',context)
    else:
        orders = Order.objects.all().order_by('-created_at')
        for order in orders:
            if order.discount_price != 0:
                order.final_price = order.order_total-order.discount_price
                order.save()
            else:
                pass
        paginator = Paginator(orders, 10)
        page = request.GET.get('page')
        orders_page = paginator.get_page(page)


        context = {
            'orders_page': orders_page,
        }
        return render(request,'admintemplates/reports.html',context)


def admin_invoice(request,order_id):

    orders = Order.objects.get(id=order_id)
    total = orders.order_total+orders.tax
    grand_total = round(total-float(orders.discount_price),2)
    discount_price=orders.discount_price
    context = {
        'orders':orders,
        'grand_total':grand_total,
        'discount_price':discount_price
    }
    return render(request,'admintemplates/invoiceforadmin.html',context)

