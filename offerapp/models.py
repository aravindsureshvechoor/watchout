from django.db import models
from ecommerce.models import Account
from siteadmin.models import Category

# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=50,unique=True)
    startdate = models.DateField(auto_now_add=True)
    enddate = models.DateField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.code
    
class AppliedCoupon(models.Model):
    currentuser = models.ForeignKey(Account, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)

class CategoryOffer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    startdate = models.DateField(auto_now_add=True)
    enddate = models.DateField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.category
    