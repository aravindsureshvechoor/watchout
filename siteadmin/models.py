from django.db import models
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):

    category_name = models.CharField(max_length=50, unique=True)
    slug          = models.SlugField(max_length=100, unique=True)
    description   = models.TextField(max_length=255, blank=True)
    is_available  = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'category'
        verbose_name_plural = 'categories'
    
    def get_url(self):
        return reverse('products_by_category',args=[self.slug])

    
    def save(self, *args, **kwargs):
        # Automatically generate the slug from the product name
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.category_name

class Product(models.Model):

    product_name  = models.CharField(max_length=200, unique=True)
    slug          = models.SlugField(max_length=200, unique=True)
    description   = models.TextField(max_length=500, blank=True , null=True)
    price         = models.DecimalField(max_digits=5, decimal_places=2)
    offerprice    = models.DecimalField(max_digits=5, decimal_places=2,blank=True)
    images        = models.ImageField(upload_to='photos/products')
    stock         = models.IntegerField()
    is_available  = models.BooleanField(default=True)
    category      = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date  = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail',args=[self.category.slug, self,slug])


        
    def save(self, *args, **kwargs):
        # Automatically generate the slug from the product name
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)



    def __str__(self):
        return self.product_name

