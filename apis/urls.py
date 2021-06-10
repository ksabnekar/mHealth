from django.conf.urls import include, url

from apis import views

urlpatterns = [
	url(r'^categories_list/', views.categories_list, name='categories_list'),
    url(r'^add_category/', views.add_category, name='add_category'),
    url(r'^update_category/', views.update_category, name='update_category'),
    url(r'^delete_category/', views.delete_category, name='delete_category'),
    url(r'^login_admin_user/', views.login_admin_user, name='login_admin_user'),

    url(r'^add_resource/', views.add_resource, name='add_resource'),
    url(r'^update_resource/', views.update_resource, name='update_resource'),
    url(r'^delete_resource/', views.delete_resource, name='delete_resource'),
    url(r'^add_user_location/', views.add_user_location, name='add_user_location'),
    url(r'^export_user_locations/', views.export_user_locations, name='export_user_locations'),
]
