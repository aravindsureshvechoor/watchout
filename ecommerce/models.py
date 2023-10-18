from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from siteadmin.models import *
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,user_name,email,password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not user_name:
            raise ValueError('User must have a username')

        user = self.model(
            email       = self.normalize_email(email),
            user_name   = user_name,
            first_name  = first_name,
            last_name   = last_name,
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,first_name,last_name,email,user_name,password):
        user = self.create_user(
            email = self.normalize_email(email),
            user_name = user_name,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
        

class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    user_name       = models.CharField(max_length=50,unique=True)
    email           = models.EmailField(max_length=254,unique=True)
    # phone_number    = models.CharField(max_length=50, null=True, blank=True)


    #required
    profilepic        = models.ImageField(upload_to='photos/profilepic')
    date_joined       = models.DateTimeField(auto_now_add=True)
    last_login        = models.DateTimeField(auto_now_add=True)
    is_admin          = models.BooleanField(default=True)
    is_staff          = models.BooleanField(default=True)
    is_active         = models.BooleanField(default=False)
    is_superuser      = models.BooleanField(default=True)
    is_blocked        = models.BooleanField(default=False)
    
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['user_name','first_name','last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,add_label):
        return True

class UserAddress(models.Model):
    
    currentuser = models.ForeignKey(Account, on_delete=models.CASCADE)
    firstname   = models.CharField(max_length=50)
    lastname    = models.CharField(max_length=50)
    email       = models.EmailField(max_length=254)
    phone       = models.IntegerField()
    homeaddress = models.TextField()
    city        = models.CharField(max_length=50)
    pincode     = models.IntegerField()
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return  f"{self.currentuser}'s Address"

class Payment(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	payment_id = models.CharField(max_length=100)
	order_number = models.CharField(max_length=50)
	payment_method = models.CharField(max_length=100)
	amount_payed = models.CharField(max_length=100)
	status = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.payment_method  

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    homeaddress = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    final_price = models.FloatField(blank=True)
    order_total = models.FloatField()
    discount_price=models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    def full_name(self):
        return f'{self.firstname} {self.lastname}'

    def full_address(self):
        return f'{self.homeaddress}'

class OrderProduct(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	product_price = models.FloatField()
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	ordered = models.BooleanField(default=False)
	returned = models.BooleanField(default=False)



class Feedback(models.Model):
    currentuser = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class Wallet(models.Model):
    amount = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
    currentuser = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.amount
    
class Referalid(models.Model):
    referalid = models.CharField(max_length=50)
    currentuser = models.ForeignKey(Account, on_delete=models.CASCADE)


    def __str__(self):
        return self.referalid
    
