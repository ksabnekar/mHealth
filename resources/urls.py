from django.urls import path, re_path
from . import views
from django.conf.urls import url

urlpatterns = [

    path('/categorylist', views.category_list, name='category_list'),
    #path('/location', views.Home.as_view(), name='location'),
    path('', views.home, name='home'),
    path('resource_list/<int:pk>/', views.resource_list, name='resource_list'),
    path('resource_list_by_location/<str:category_id>/<str:lat>/<str:lon>/', views.resource_list_by_location, name='resource_list_by_location'),
    path('/feedback', views.feedback, name='feedback'),
    path('/about_us', views.about_us, name='about_us'),
]