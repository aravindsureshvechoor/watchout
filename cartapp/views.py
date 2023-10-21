from django.shortcuts import render,redirect,HttpResponse
from .models import *
from siteadmin.models import *
from ecommerce.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ecommerce.decorators import never_cache
from offerapp.models import *
from django.contrib.sessions.models import Session
import random
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta, datetime, time, timedelta, date
from django.http import JsonResponse
from decimal import Decimal
from django.core.mail import send_mail


def _cart_id(request):  
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

@never_cache
@login_required(login_url='usersignin')
def cart(request,total=0,quantity=0,cart_items=None):

    if request.user.is_authenticated:
        tax = 0
        grandtotal = 0
        total = 0
        cart_items = CartItem.objects.filter(is_active=True,currentuser=request.user)

        for cart_item in cart_items:
            # if cart_item.product.offerprice != 0:
            total += round((cart_item.product.offerprice * cart_item.quantity),2)
            # else:
            #     total += round((cart_item.product.price * cart_item.quantity),2)
            quantity += cart_item.quantity
        tax = round(total/100 * 15,2)
        grandtotal = round(tax + total,2)

        context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'tax':tax,
            'grandtotal':grandtotal
        }

        return render(request,'carttemplates/shop-cart.html',context)

    else:
        messages.error(request,'You should Signin first to add an item to your cart')
        return redirect('usersignin')

@never_cache
@login_required(login_url='usersignin')
def add_to_cart(request,product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id) #get the product

        if product.is_available == True:

            try:
                cart = uCart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
            except uCart.DoesNotExist:
                cart = uCart.objects.create(
                    cart_id = _cart_id(request)
                )
            cart.save()

            try:
                cart_item = CartItem.objects.get(currentuser=request.user,product=product)
                cart_item.quantity += 1 
                if cart_item.product.stock < cart_item.quantity:
                    messages.error(request,'Out of Stock')
                else:
                    cart_item.save()

            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
                currentuser = request.user,
                )
                cart_item.save()

            tax = 0
            grandtotal = 0
            total = 0
            quantity = 0
            cart_items = CartItem.objects.filter(is_active=True,currentuser=request.user)

            for cart_item1 in cart_items:
                # if cart_item1.product.offerprice != 0:
                total += round((cart_item1.product.offerprice * cart_item1.quantity),2)
                # else:
                #     total += round((cart_item1.product.price * cart_item1.quantity),2)
                quantity += cart_item1.quantity
            tax = round(total/100 * 15,2)
            grandtotal = round(tax + total,2)

            context = {
                'total':total,
                'quantity':quantity,
                'cart_items':cart_items,
                'tax':tax,
                'grandtotal':grandtotal
            }

            messages.success(request,"Item added to cart")
            return redirect('cart')

        elif product.is_available==False:
            messages.success(request,'Product is currently unavailable')
            return redirect('shop')
    else:   
        messages.error(request,'You should Signin first to add an item to your cart')
        return redirect('usersignin')


@never_cache
@login_required(login_url='usersignin')
def add_cart(request,product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id) #get the product

        try:
            cart = uCart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except uCart.DoesNotExist:
            cart = uCart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        try:
            cart_item = CartItem.objects.get(currentuser=request.user,product=product)
            cart_item.quantity += 1 
            if cart_item.product.stock < cart_item.quantity:
                messages.error(request,'Out of Stock')
            else:
                cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
            currentuser = request.user,
            )
            cart_item.save()

        tax = 0
        grandtotal = 0
        total = 0
        quantity = 0
        cart_items = CartItem.objects.filter(is_active=True,currentuser=request.user)

        for cart_item1 in cart_items:
            # if cart_item1.product.offerprice != 0:
            total += round((cart_item1.product.offerprice * cart_item1.quantity),2)
            # else:
            #     total += round((cart_item1.product.price * cart_item1.quantity),2)
            quantity += cart_item1.quantity
        tax = round(total/100 * 15,2)
        grandtotal = round(tax + total,2)

        # context = {
        #     'total':total,
        #     'quantity':quantity,
        #     'cart_items':cart_items,
        #     'tax':tax,
        #     'grandtotal':grandtotal
        # }
        # if cart_item.product.offerprice!=0:
        prd_total=round(float(cart_item.quantity)*float(cart_item.product.offerprice),2)
        # else:
        #     prd_total=round(float(cart_item.quantity)*float(cart_item.product.price),2)

        return JsonResponse({
            
            'quantity': cart_item.quantity,
            # 'prd_total':float(cart_item.quantity)*float(cart_item.product.price),
            'prd_total':prd_total,
            'total': total,
            'tax': tax,
            'grandtotal':grandtotal,
        })




        # return redirect('cart')

    else:   
        messages.error(request,'You should Signin first to add an item to your cart')
        return redirect('usersignin')



@never_cache
@login_required(login_url='usersignin')
def wishlist(request):
    items = WishlistItem.objects.filter(currentuser=request.user)
    context = {

        'items':items
            }

    return render(request,'carttemplates/wishlist.html',context)

@never_cache
@login_required(login_url='usersignin')
def addtowishlist(request,product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        try:
            item = WishlistItem.objects.get(product=product,currentuser=request.user)
            if item:
                messages.success(request,'Item is already in the wishlist')  
                return redirect('shop')
            else:
                wishlist_item = WishlistItem.objects.create(
                        product=product,
                        currentuser=request.user,
                        is_active=True, 
                    )
                wishlist_item.save()
                messages.success(request,'Added to wishlist')
                return redirect('wishlist')
        except:
            wishlist_item = WishlistItem.objects.create(
                    product=product,
                    currentuser=request.user,
                    is_active=True, 
                )
            wishlist_item.save()
            messages.success(request,'Added to wishlist')
            return redirect('wishlist')
    else:
        messages.error(request,'Log in to add a product to wishlist')
        return redirect('usersignin')

@never_cache
@login_required(login_url='usersignin')
def removefromwishlist(request,wishlist_id):
    item = WishlistItem.objects.get(id=wishlist_id)
    item.delete()
    messages.success(request,'Item removed from wishlist')

    return redirect('wishlist')

@never_cache
@login_required(login_url='usersignin')
def cartdecrement(request,cart_id):
    try:
        # product = Product.objects.get(id=product_id)
        # cart = uCart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(currentuser=request.user,id=cart_id)
        if cart_item.quantity>1:
            cart_item.quantity -= 1 
            cart_item.save()
        else:
            pass
    except ObjectDoesNotExist:
        pass

    tax = 0
    grandtotal = 0
    total = 0
    quantity = 0
    cart_items = CartItem.objects.filter(is_active=True,currentuser=request.user)

    for cart_item1 in cart_items:
        # if cart_item1.product.offerprice != 0:
        total += round((cart_item1.product.offerprice * cart_item1.quantity),2)
        # else:
        #     total += round((cart_item1.product.price * cart_item1.quantity),2)

        quantity += cart_item1.quantity
    tax = round(total/100 * 15,2)
    grandtotal = round(tax + total,2)

    # context = {
    #     'total':total,
    #     'quantity':quantity,
    #     'cart_items':cart_items,
    #     'tax':tax,
    #     'grandtotal':grandtotal
    # }
    # if cart_item.product.offerprice != 0:
    prd_total=round(float(cart_item.quantity)*float(cart_item.product.offerprice),2)
    # else:
    #     prd_total=round(float(cart_item.quantity)*float(cart_item.product.price),2)

    return JsonResponse({
        
        'quantity': cart_item.quantity,
        # 'prd_total':float(cart_item.quantity)*float(cart_item.product.price),
        'prd_total':prd_total,
        'total': total,
        'tax': tax,
        'grandtotal':grandtotal,
    })
    # return redirect('cart')




@never_cache
@login_required(login_url='usersignin')
def removeitem(request,cart_id):
    try:
        cart_item = CartItem.objects.get(id=cart_id)
        cart_item.delete()
        
    except ObjectDoesNotExist:
        pass
    messages.success(request,"Item removed from cart")
    return redirect('cart')

    

@never_cache
@login_required(login_url='usersignin')
def checkout(request):
    tax = 0
    grandtotal = 0
    total = 0
    currentuser = request.user
    quantity = 0
    cart_items = CartItem.objects.filter(currentuser=currentuser)


    for cart_item in cart_items:
        if cart_item.product.is_available == True:
            if cart_item.product.offerprice != cart_item.product.price:
                total += round((cart_item.product.offerprice * cart_item.quantity))
            else:   
                total += round((cart_item.product.price * cart_item.quantity))
            quantity += cart_item.quantity
        else:
            messages.success(request,'Please Check if every products are available')
            return redirect('cart')
    try:
        tax = round(total/100 * 15)
        grandtotal = round(tax + total)

        try:
            address = UserAddress.objects.get(is_default=True,currentuser=request.user)
        except:
            address=None

        context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'tax':tax,
            'grandtotal':grandtotal,
            'address':address
        }


        return render(request,'carttemplates/checkout.html',context)
    except:
        messages.success(request,'Unavailable')
        return redirect('cart')

@never_cache
@login_required(login_url='usersignin')
def selectaddress(request):
    addresses = UserAddress.objects.filter(currentuser=request.user)
    context = {
        'addresses':addresses
    }

    return render(request,'carttemplates/useraddress.html',context)

@never_cache
@login_required(login_url='usersignin')
def selectaddressview(request):

    adrs = UserAddress.objects.filter(currentuser=request.user)

    for ad in adrs:
        ad.is_default = False
        ad.save()

    addressid = request.GET.get('address_id')
    address = UserAddress.objects.get(id=addressid)
    address.is_default = True
    address.save()
    context = {
        'address':address
    }

    return redirect('checkout')

@never_cache
@login_required(login_url='usersignin')
def placeorder(request, total=0,quantity=0):
  
    cur_user = request.user
    cart_items = CartItem.objects.filter(currentuser=cur_user)
    cart_count = cart_items.count()
    if cart_count <= 0:

        messages.warning(request, 'Your Cart is Empty!')
        return redirect('checkout')

    grant_total = 0
    tax = 0
    total,quantity=0,0
    total_1,quantity_1 =0,0

    for cart_item in cart_items:
        if cart_item.product.offerprice != cart_item.product.price:
            total_1 += round((cart_item.product.offerprice * cart_item.quantity))
        else:
            total_1 += round((cart_item.product.price * cart_item.quantity))
        quantity_1 += cart_item.quantity
 
    tax_1 = round((total_1/100)*15)
    grant_total_1=total_1+tax_1
    try:
        address = UserAddress.objects.get(currentuser=request.user, is_default=True)

    except:
        messages.info(request, 'No Address Present or Selected,Please Add Address and Comeback before placing order')

        return redirect('checkout')

    if request.method == 'POST':

        # form = OrderForm(request.POST)
        payment = Payment.objects.create(
            user=request.user,
            payment_method = 'not paid',
        )
        payment.save()

        data = Order()
        data.user=request.user
        data.firstname = address.firstname
        data.lastname = address.lastname
        data.phone = address.phone
        data.email = address.email
        data.payment = payment
        data.homeaddress = address.homeaddress
        data.city = address.city
        data.pincode = address.pincode
        data.discount_price=0
        data.order_total = grant_total_1
        data.final_price = grant_total_1
        data.tax = tax_1
        data.ip = request.META.get('REMOTE_ADDR')
        data.is_ordered = False
        data.save()

        #Generating Order Number
        yr = int(date.today().strftime('%Y'))
        dt = int(date.today().strftime('%d'))
        mt = int(date.today().strftime('%m'))
        d = date(yr,mt,dt)
        cur_date = d.strftime('%Y%m%d')
        order_number = cur_date + str(data.id)
        data.order_number = order_number
        data.save()


        for item in cart_items:
            if item.product.offerprice != item.product.price:
                product_price  = item.product.offerprice
            else:
                product_price  = item.product.price

            order_product=OrderProduct.objects.create(
                user=request.user,
                product=item.product,
                # product_price=(item.product.price * item.quantity),
                product_price=product_price,
                quantity=item.quantity,
                order=data
            )
            order_product.save()
           
        

        order = Order.objects.get(user=cur_user, order_number=order_number)
        order_items = OrderProduct.objects.filter(order=order)
        order_total = round(order.order_total,2)
        quantity = 0
        request.session['grand_total']=order_total
        for item in order_items:
            total += item.product_price
            quantity += item.quantity

        tax = (total/100)*15
        grant_total=total+tax
        context = {
            'order': order,
            'order_items': order_items,
            'total': total,
            'tax': order.tax,
            # 'grand_total': order.order_total,
            'grand_total':order_total
        }
    return render(request,'carttemplates/payment.html',context)

@never_cache
@login_required(login_url='usersignin')
def cashondelivery(request):
    order_id = request.GET.get('ordr_id')
    cur_user = request.user
    order = Order.objects.get(id=order_id)
    order.is_ordered = True
    order.payment.payment_method = 'COD'
    order.payment.save()
    order.save()
    cart_item = CartItem.objects.filter(currentuser=cur_user)
    cart_item.delete()

    account = Account.objects.get(email=request.user)
    subject = "Order Placed"
    email   = account.email
    sendermail = "Watchout Ecommerce Store"
    message = f"An order has been placed , Please login to your account for more information , Thank You {account.first_name} ."
    details = f"{message}"
    send_mail(subject,details,sendermail,[email])

    context = {'order':order}
    return redirect('myorders')

@never_cache
@login_required(login_url='usersignin')
def walletpayment(request):
    
    wallet = Wallet.objects.get(currentuser=request.user)
    order_id = request.GET.get('ordr_id')
    cur_user = request.user
    order = Order.objects.get(id=order_id)
    grand_total = request.session['grand_total']
    if grand_total <= wallet.amount:
        order.is_ordered = True
        order.payment.payment_method = 'Wallet'
        order.payment.save()
        order.save()
        cart_item = CartItem.objects.filter(currentuser=cur_user)
        cart_item.delete()
        wallet.amount -= grand_total
        wallet.save()
        messages.success(request,'Order success')

        account = Account.objects.get(email=request.user)
        subject = "Order Placed"
        email   = account.email
        sendermail = "Watchout Ecommerce Store"
        message = f"An order has been placed , Please login to your account for more information , Thank You {account.first_name} ."
        details = f"{message}"
        send_mail(subject,details,sendermail,[email])

        return redirect('myorders')
    else:
        messages.success(request,'Not enough amount in your wallet')
        return redirect('wallet')

@never_cache
@login_required(login_url='usersignin')  
def myorders(request):
    current_user = request.user
 
    user = Account.objects.get(email=current_user)
    orders = Order.objects.filter(user_id=user,is_ordered =True).order_by('-created_at')
    context = {
        'orders':orders,
        
    }
    return render(request, 'carttemplates/orders.html', context)

@never_cache
@login_required(login_url='usersignin')
def cancelorder(request,order_id):
    order = Order.objects.get(id=order_id)
    order.status = "Cancelled"
    order.save()


    if Wallet.objects.filter(currentuser=request.user).exists() and order.payment.payment_method == "Razorpay" or order.payment.payment_method == "Wallet" :
        wallet = Wallet.objects.get(currentuser=request.user)
        wallet.amount += round(float(order.order_total+order.tax)-float(order.discount_price),2)
        wallet.save()
        return redirect(myorders)
    else:
        if order.payment.payment_method == "Razorpay" or order.payment.payment_method == "Wallet" :
            Wallet.objects.create(currentuser=request.user,
            amount = round(float(order.order_total+order.tax)-float(order.discount_price),2)
            )

            return redirect(myorders)
        else:
            return redirect(myorders)

@never_cache
@login_required(login_url='usersignin')
def returnorder(request,order_id):
    order = Order.objects.get(id=order_id)
    order.status = "Returned"
    order.save()

    if Wallet.objects.filter(currentuser=request.user).exists():
        wallet = Wallet.objects.get(currentuser=request.user)
        wallet.amount += round(float(order.order_total+order.tax)-float(order.discount_price),2)
        wallet.save()

    else:
        Wallet.objects.create(currentuser=request.user,
        amount = round(float(order.order_total+order.tax)-float(order.discount_price),2)
        )

    return redirect(myorders)

@never_cache
@login_required(login_url='usersignin')
def orderdetails(request,order_id):
    order = Order.objects.get(id=order_id)
    orderproduct = OrderProduct.objects.filter(order=order)
    if order.discount_price:
        grand_total = round((order.order_total+order.tax) - order.discount_price,2)
    else:
        grand_total = round(order.order_total + order.tax,2)
    context = {
        'orderproduct':orderproduct,
        'order':order,
        'grand_total':grand_total,

    }
   
    return render(request,'carttemplates/orderdetails.html',context)

@never_cache
@login_required(login_url='usersignin')
def razorpay_payment(request,orderNumber):
    order = Order.objects.get(order_number=orderNumber) 
    cur_user = request.user
    order.is_ordered = True
    try:
        order.discount_price = request.session['discount_amount']
    except:
        order.discount_price = 0
    order.save()
    cart_item = CartItem.objects.filter(currentuser=cur_user)
    cart_item.delete()
    
    payment = order.payment
    #Generating transaction Number
    yr = int(date.today().strftime('%Y'))
    dt = int(date.today().strftime('%d'))
    mt = int(date.today().strftime('%m'))
    d = date(yr,mt,dt)
    cur_date = d.strftime('%Y%m%d')
    payment_id = "RZRP"+str(payment.id)+cur_date 
    payment.payment_id=payment_id
    payment.amount_payed=order.order_total + order.tax
    payment.payment_method = "Razorpay"
    payment.status = "Completed"
    payment.save()
    ordered_products = OrderProduct.objects.filter(order=order)
    print("orderNumber======",orderNumber)

    account = Account.objects.get(email=request.user)
    subject = "Order Placed"
    email   = account.email
    sendermail = "Watchout Ecommerce Store"
    message = f"An order has been placed , Please login to your account for more information , Thank You {account.first_name} ."
    details = f"{message}"
    send_mail(subject,details,sendermail,[email])
    


    context = {
        'order':order,
        'transID':payment_id,
        'payment':payment,
        'ordered_products':ordered_products

    }


    return render(request,'carttemplates/invoice.html',context)

@never_cache
@login_required(login_url='usersignin')
def applycoupon(request):
    if request.method == "POST":
        order_id = request.POST['order_id']
        code = request.POST['coupon_obj']
        coupon = None
        if Coupon.objects.filter(code=code).exists():
            coupon = Coupon.objects.get(code=code)
        else:
            messages.warning(request,'Coupon does not exist')
            return redirect('payment_page', order_id)

        try:

            is_applied = AppliedCoupon.objects.get(currentuser=request.user,coupon=coupon)
            messages.error(request,'Coupon already applied')
            return redirect('payment_page', order_id)
            
        except:
            
            AppliedCoupon.objects.create(currentuser=request.user,coupon=coupon)
            order = Order.objects.get(id=order_id)
        
            grand_total = order.order_total
            discount = coupon.discount_percentage
            newamount = float(grand_total - ((float(grand_total) / 100) * float(discount)))
            order.order_total = round(Decimal(newamount))
            order.save()
            request.session['discount_amount'] = round(((float(grand_total) / 100) * float(discount)))
            request.session['coupon_code']=code
            return redirect('payment_page', order_id)


           

@never_cache
@login_required(login_url='usersignin')
def payment_page(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderProduct.objects.filter(order=order)
    quantity = 0
    total = 0

    try:
        discount_amount = request.session['discount_amount']
    except:
        discount_amount = 0
    

    for item in order_items:
        total += item.product_price
        quantity += item.quantity

    tax = (total/100)*15
    grant_total=round(total+tax)
    context = {
        'order': order,
        'order_items': order_items,
        'total': total,
        'tax': order.tax,
        'grand_total': order.order_total,
        'discount_amount':round(discount_amount)
    }
    return render(request,'carttemplates/payment.html',context)
