from django.contrib import admin
from .import views
from django.urls import path,include


urlpatterns = [

    path('cart',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('checkout',views.checkout,name='checkout'),
    path('placeorder/razorpay_payment/<str:orderNumber>/',views.razorpay_payment,name='razorpay_payment'),
    path('cartdecrement/<int:cart_id>/',views.cartdecrement,name='cartdecrement'),
    path('removeitem/<int:cart_id>/',views.removeitem,name='removeitem'),
    path('selectaddress',views.selectaddress,name='selectaddress'),
    path('selectaddressview',views.selectaddressview,name='selectaddressview'),
    path('placeorder',views.placeorder,name='placeorder'),
    path('cashondelivery',views.cashondelivery,name='cashondelivery'),
    path('myorders',views.myorders,name='myorders'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('addtowishlist/<int:product_id>/',views.addtowishlist,name='addtowishlist'),
    path('removefromwishlist/<int:wishlist_id>/',views.removefromwishlist,name='removefromwishlist'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('cancelorder/<int:order_id>/',views.cancelorder,name='cancelorder'),
    path('returnorder/<int:order_id>/',views.returnorder,name='returnorder'),
    path('orderdetails/<int:order_id>/',views.orderdetails,name='orderdetails'),
    path('applycoupon',views.applycoupon,name='applycoupon'),

    path('payment_page/<int:order_id>/',views.payment_page,name='payment_page'),

    

]

