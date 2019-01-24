from django.conf.urls import patterns, url
from Foodie import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^upload/', views.upload, name= 'upload'),
        url(r'^about/', views.about, name= 'about'),
        url(r'^location/', views.location, name= 'location'),
        url(r'^special/', views.special, name= 'special'),
        url(r'^privacy/', views.privacy, name= 'privacy'),
        url(r'^contact/', views.contact, name= 'contact'),
        url(r'^page/(?P<page_name_slug>[\w\-]+)/$', views.page, name='category'),
        #url(r'^upload_csv', views.upload, name = 'upload'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^register/$', views.register, name='register'),
        )