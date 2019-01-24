from django.contrib import admin
from Foodie.models import Category, Page
from django.db import models
from django.contrib.auth.models import User


class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'views', 'midprice','premiumprice','regularprice','feature','special','address','des','image')
    list_editable = ('feature',)
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank = True)

    def __unicode__(self):
        return self.user.username


admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Page, PageAdmin)