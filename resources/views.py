from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
import json
from .serializers import *
from django.db import connection


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def resource_list_by_location(request, category_id, lat, lon):
    #resources = Resources.objects.filter(category_id = category_id)
    cursor = connection.cursor()
    cursor.execute("select * from (SELECT  *,( 3959 * acos( cos( radians("+lat+") ) * cos( radians( latitude ) ) * cos( radians( longitude ) - radians("+lon+") ) + sin( radians("+lat+") ) * sin( radians( latitude ) ) ) ) AS distance FROM resources_resources) al where distance < 100 and category_id = "+category_id+" ORDER BY distance limit 5");
    listTemp = dictfetchall(cursor)
    cursor.close()
    category = Category.objects.filter(status = 1)
    return render(request, 'resources/index.html',
                 {'categories': category, 'resources': listTemp, "resources2": json.dumps(listTemp), "latitude" : lat, "longitude" : lon})

def home(request):
    category = Category.objects.filter(status = 1)
    return render(request, 'resources/home.html', {'categories': category})

def category_list(request):
    category = Category.objects.filter(status = 1)
    return render(request, 'resources/category_list.html',
                 {'categories': category})

def resource_list(request,pk):
    resource = Resources.objects.filter(category_id=pk, status = 1)
    category = Category.objects.get(category_id = pk)
    categories = Category.objects.filter(status = 1)
    return render(request, 'resources/resource_list.html',
                 {'categories': categories, 'resources': resource, 'category_id': pk, 'category_name': category.category_name})

def feedback(request):
    category = Category.objects.filter(status = 1)
    return render(request, 'resources/feedback.html', {'categories': category})

def about_us(request):
    category = Category.objects.filter(status = 1)
    return render(request, 'resources/about_us.html',
                 {'categories': category})
