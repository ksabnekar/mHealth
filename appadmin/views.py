from django.shortcuts import render
from django.db import transaction
from rest_framework.authtoken.models import Token
from resources.models import *
from resources.serializers import *
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def set_session_null_for_app_admin(request):
    if request.session.get('token', False):
        del request.session['token']
    return redirect("index")

def login(request):
    return render(request, "login.html", {})

def dashboard(request):
    with transaction.atomic():
        token = None
        if 'token' in request.POST.keys():
            token = request.POST['token']
            request.session['token'] = token
        if token is None and request.session['token'] is not None:
            token = request.session['token']
        if token is not None:
            token1 = Token.objects.get(key=token)
            user = token1.user
            return render(request, "dashboard.html", {"token":token})
        else:
            return redirect("set_session_null_for_app_admin")
        
def categories(request):
    with transaction.atomic():
        token = request.session['token']
        token1 = Token.objects.get(key=token)
        user = token1.user
        if user is not None:
            return render(request, "categories.html", {})
        else:
            return redirect("set_session_null_for_app_admin")

def resources(request):
    with transaction.atomic():
        token = request.session['token']
        token1 = Token.objects.get(key=token)
        user = token1.user
        if user is not None:
            categories_list = Category.objects.filter(status = 1)
            c_serializer = CategorySerializer(categories_list, many = True).data
            resources_list = Resources.objects.filter(status = 1)
            r_serializer = ResourcesSerializer(resources_list, many = True).data
            return render(request, "resources.html", {"resources" : json.dumps(r_serializer, cls=DjangoJSONEncoder), "categories" : json.dumps(c_serializer, cls=DjangoJSONEncoder)})
        else:
            return redirect("set_session_null_for_app_admin")

def add_resource(request):
    with transaction.atomic():
        token = request.session['token']
        token1 = Token.objects.get(key=token)
        user = token1.user
        if user is not None:
            categories_list = Category.objects.filter(status = 1)
            c_serializer = CategorySerializer(categories_list, many = True).data
            return render(request, "add_resource.html", {"categories" : json.dumps(c_serializer, cls=DjangoJSONEncoder)})
        else:
            return redirect("set_session_null_for_app_admin")

def view_resource(request):
    with transaction.atomic():
        token = request.session['token']
        token1 = Token.objects.get(key=token)
        user = token1.user
        if user is not None:
            resourceId = request.POST['viewResourceId']
            categories_list = Category.objects.filter(status = 1)
            c_serializer = CategorySerializer(categories_list, many = True).data
            return render(request, "view_resource.html", {"resourceId":resourceId, "categories" : json.dumps(c_serializer, cls=DjangoJSONEncoder)})
        else:
            return redirect("set_session_null_for_app_admin")

def edit_resource(request):
    with transaction.atomic():
        token = request.session['token']
        #if checkAuthentication(token):
        token1 = Token.objects.get(key=token)
        user = token1.user
        if user is not None:
            resourceId = request.POST['editResourceId']
            categories_list = Category.objects.filter(status = 1)
            c_serializer = CategorySerializer(categories_list, many = True).data
            return render(request, "edit_resource.html", {"resourceId":resourceId, "categories" : json.dumps(c_serializer, cls=DjangoJSONEncoder)})
        else:
            return redirect("set_session_null_for_app_admin")

def user_locations(request):
    with transaction.atomic():
        token = request.session['token']
        token1 = Token.objects.get(key=token)
        user = token1.user
        if user is not None:
            user_locations = UserLocations.objects.all()
            user_locations_serializer = UserLocationsSerializer(user_locations, many = True).data
            return render(request, "user_locations.html", {"user_locations" : json.dumps(user_locations_serializer, cls=DjangoJSONEncoder)})
        else:
            return redirect("set_session_null_for_app_admin")