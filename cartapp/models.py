from django.db import models
from siteadmin.models import *
from ecommerce.models import *

# Create your models here.class Cart

class uCart(models.Model):

    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(uCart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    currentuser = models.ForeignKey(Account, on_delete=models.CASCADE)
    def sub_total(self):
        return self.quantity * (self.product.price)

    def __str__(self):
        return self.product.product_name

class WishlistItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    currentuser = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.product_name


    

    
    

