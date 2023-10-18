from django.contrib import admin
from .import views
from django.urls import path,include


urlpatterns = [

    path('',views.home,name='home'),
    path('usersignup',views.usersignup,name='usersignup'),
    path('usersignin',views.usersignin,name='usersignin'),
    path('usersignout',views.signout,name='signout'),
    path('otp',views.otp,name='otp'),
    path('contact',views.contact,name='contact'),
    path('shop',views.shop,name='shop'),
    path('productinfo/<int:product_id>/',views.productinfo,name='productinfo'),
    path('accountinfo',views.accountinfo,name='accountinfo'),
    path('editaccountinfo',views.editaccountinfo,name='editaccountinfo'),
    path('saveuseredit',views.saveuseredit,name='saveuseredit'),
    path('discarduseredit',views.discarduseredit,name='discarduseredit'),
    path('addaddress',views.addaddress,name='addaddress'),
    path('submitaddress',views.submitaddress,name='submitaddress'),
    path('editaddress',views.editaddress,name='editaddress'),
    path('editaddressview',views.editaddressview,name='editaddressview'),
    path('addresssave',views.addresssave,name='addresssave'),
    path('addressdelete',views.addressdelete,name='addressdelete'),
    path('discard',views.discard,name='discard'),
    path('productsorting',views.productsorting,name='productsorting'),
    path('feedback/<int:product_id>/',views.feedback,name='feedback'),
    path('addfeedback/<int:product_id>/',views.addfeedback,name='addfeedback'),
    path('coupondetails',views.coupondetails,name='coupondetails'),
    path('search',views.search,name='search'),
    path('invoice/<int:order_id>/',views.invoice,name='invoice'),
    path('wallet',views.wallet,name='wallet'),
    path('profilepic',views.profilepic,name='profilepic'),

]