from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from decimal import Decimal



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(default='')

    def save(self, *args, ** kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=128)
    views = models.IntegerField(max_length=10, default= 0)
    midprice = models.DecimalField(max_digits=5,decimal_places=2,default= 0)
    premiumprice = models.DecimalField(max_digits=5,decimal_places=2,default= 0)
    regularprice = models.DecimalField(max_digits=5,decimal_places=2,default= 0)
    feature = models.BooleanField(default=False)
    special = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    des = models.CharField(max_length=9999)
    image = models.ImageField(upload_to='static/images/', default ='static/images/logo_zB8KZxe.png') # jpeg might work better.
    slugP = models.SlugField(default='')

    def save(self, *args, ** kwargs):
        self.slugP = slugify(self.name)
        super(Page, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'views', 'price','image')

