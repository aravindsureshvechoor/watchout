from django.contrib import admin
from .import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('admin-home',views.adminsignin,name='adminhome'),
    path('admin-logout',views.adminlogout,name='adminlogout'),


    path('product-management',views.productmanagement,name='productmanagement'),
    path('user-management',views.usermanagement,name='usermanagement'),
    path('category-management',views.categorymanagement,name='categorymanagement'),

    path('editcategory',views.editcategory,name='editcategory'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('deletecategory',views.deletecategory,name='deletecategory'),

    path('admin-dashboard',views.admindashboard,name='admindashboard'),
    path('blockuser',views.blockuser,name='blockuser'),
    path('unblockuser',views.unblockuser,name='unblockuser'),
    path('deleteuser',views.deleteuser,name='deleteuser'),
    
    path('addproduct',views.addproduct,name='addproduct'),
    path('deleteproduct',views.deleteproduct,name='deleteproduct'),
    path('editproduct',views.editproduct,name='editproduct'),
    path('discardproductchanges',views.discardproductchanges,name='discardproductchanges'),
    path('discardcategorychanges',views.discardcategorychanges,name='discardcategorychanges'),
    path('discardcouponchanges',views.discardcouponchanges,name='discardcouponchanges'),
    path('ordermanagement',views.ordermanagement,name='ordermanagement'),
    path('admin_change_order_status/<order_id>/',views.admin_change_order_status,name='admin_change_order_status'),
    path('coupon',views.coupon,name='coupon'),
    path('addcoupon',views.addcoupon,name='addcoupon'),
    path('editcoupon/<coupon_id>/',views.editcoupon,name='editcoupon'),
    path('deletecoupon',views.deletecoupon,name='deletecoupon'),
    path('categoryoffer',views.categoryoffer,name='categoryoffer'),
    path('addcategoryoffer',views.addcategoryoffer,name='addcategoryoffer'),
    path('editcategoryoffer/<category_id>/',views.editcategoryoffer,name='editcategoryoffer'),
    path('deletecategoryoffer/<category_id>/',views.deletecategoryoffer,name='deletecategoryoffer'),
    path('discardedit',views.discardedit,name='discardedit'),
    path('chart',views.chart,name='chart'),
    path('reports',views.reports,name='reports'),
    path('admin_invoice/<order_id>/',views.admin_invoice,name='admin_invoice'),
    path('deactivateproduct/<product_id>/',views.deactivateproduct,name='deactivateproduct'),
    path('activateproduct/<int:product_id>/',views.activateproduct,name='activateproduct'),
    path('deactivatecategory/<int:category_id>/',views.deactivatecategory,name='deactivatecategory'),
    path('activatecategory/<int:category_id>/',views.activatecategory,name='activatecategory'),

    


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

