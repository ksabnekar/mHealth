'''
Created on 13-Oct-2017

@author: netset
'''
from django.conf.urls import include, url
from django.urls import path

from appadmin import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

urlpatterns = [
    
    url(r'^$', views.login, name='login'),
    url(r'^login/', views.login, name='login'),
    url(r'^dashboard/', views.dashboard, name='appadmindashboard'),
    url(r'^categories/', views.categories, name='appadmincategories'),
    url(r'^resources/', views.resources, name='appadminresources'),
    url(r'^add_resource/', views.add_resource, name='appadminaddresource'),
    url(r'^view_resource/', views.view_resource, name='view_resource'),
    url(r'^edit_resource/', views.edit_resource, name='edit_resource'),
    url(r'^set_session_null_for_app_admin/', views.set_session_null_for_app_admin, name='set_session_null_for_app_admin'),
    
]