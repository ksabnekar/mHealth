from django.shortcuts import render

# Create your views here.
import os
from resources.models import *
from resources.serializers import *
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
import traceback
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import datetime
from mhealth import settings
import xlsxwriter

@api_view(['GET'])
def categories_list(request):
    try:
        with transaction.atomic():
            categories = Category.objects.filter(status = 1)
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception:
        print(traceback.format_exc())
        return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_category(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)

                if user is not None:
                    try:
                        categoryCheck = Category.objects.get(category_name=request.data['category_name'], status=1)
                    except:
                        categoryCheck = None
                    if categoryCheck is None:
                        category = Category.objects.create(category_name=request.data['category_name'], status=1)
                        if category is not None:
                            return Response({"message" : "Created Successfully", "status" : "1", "object" : {"category_id" : category.category_id, "category_name" : category.category_name}}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"message" : "Something went wrong.", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
                    else:
                        return Response({"message" : "Category Already Exists!", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
                else:
                    return Response({"message" : "Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : "Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        print(traceback.format_exc())
        # transaction.rollback()
        return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['POST'])
def update_category(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)

                if user is not None:
                    serializer = CategorySerializer(data=request.data)
                    if serializer.is_valid():
                        category = Category.objects.get(pk=int(request.data['category_id']));
                        
                        if category is not None:
                            categoryCheck = Category.objects.filter(category_name=request.data['category_name']).filter(status=1).exclude(pk=int(request.data['category_id']))
                            
                            if not categoryCheck:
                                category1 = Category.objects.filter(pk=category.category_id).update(category_name=request.data['category_name'])
                                if category1 is not None:
                                    category1 = Category.objects.get(category_id=category.category_id)
                                    serializer = CategorySerializer(category1)
                                        
                                    return Response({"message" : "Updated Successfully", "status" : "1", "object" :serializer.data}, status=status.HTTP_201_CREATED)
                                else:
                                    return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            else:
                                return Response({"message" : "Category Already Exists", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({"message" : serializer.errors, "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"message" : "Somwthing went wrong", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        print(traceback.format_exc())
        # transaction.rollback()
        return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['POST'])
def delete_category(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)

                if user is not None:
                    serializer = CategorySerializer(data=request.data)
                    if serializer.is_valid():
                        category = Category.objects.get(pk=int(request.data['category_id']));
                        if category is not None:
                            category1 = Category.objects.filter(pk=category.category_id).update(status=0)
                            if category1 is not None:
                                return Response({"message" : "Successfully Deleted", "status" : "1", "object" :serializer.data}, status=status.HTTP_201_CREATED)
                            else:
                                return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        else:
                            return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        return Response({"message" : serializer.errors, "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
                else:
                    return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        print(traceback.format_exc())
        return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@csrf_exempt
def login_admin_user(request):
    try:
        with transaction.atomic():
            received_json_data = json.loads(request.body, strict=False)
            username = received_json_data['username']
            password = received_json_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active == 1:
                    token = ''
                    try:
                        user_with_token = Token.objects.get(user=user)
                    except:
                        user_with_token = None
                    
                    if user_with_token is None:
                        token1 = Token.objects.create(user=user)
                        token = token1.key
                    else:
                        Token.objects.get(user=user).delete()
                        token1 = Token.objects.create(user=user)
                        token = token1.key
                    
                    return Response({"status" : "1", "token" : token}, status=status.HTTP_200_OK)
                else:
                    return Response({"message" : "Your account has been blocked", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : "Email or Password incorrect", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        print(traceback.format_exc())
        return Response({"message" : "Sorry something went wrong.", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def resources_list(request):
    categories = list(Category.objects.all())
    return JsonResponse({'categories': categories})

@csrf_exempt
def add_category(request):
    category = Category.objects.create(category_name = request.POST['category_name'])
    return JsonResponse({'message': "Successfully Created."})

@api_view(['POST'])
def add_resource(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)

                if user is not None:
                    resource = Resources.objects.create(
                                                    resource_name = request.data['resource_name'],
                                                    eligibility = request.data['eligibility'],
                                                    resource_description = request.data['resource_description'],
                                                    office_hours = request.data['office_hours'],
                                                    phone = request.data['phone'],
                                                    location = request.data['location'],
                                                    latitude = request.data['latitude'],
                                                    longitude = request.data['longitude'],
                                                    website_link = request.data['website_link'],
                                                    category_id = request.data['category'],
                                                    status=1)
                    if resource is not None:
                        return Response({"message" : "Created Successfully", "status" : "1"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"message" : "Something went wrong.", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
                    
            
                else:
                    return Response({"message" : "Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : "Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        print(traceback.format_exc())
        # transaction.rollback()
        return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def update_resource(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)

                if user is not None:
                    resource = Resources.objects.get(pk=int(request.data['resource_id']));
                    
                    if resource is not None:
                        resource1 = Resources.objects.filter(pk=resource.resource_id).update(
                                                            resource_name = request.data['resource_name'],
                                                            eligibility = request.data['eligibility'],
                                                            resource_description = request.data['resource_description'],
                                                            office_hours = request.data['office_hours'],
                                                            phone = request.data['phone'],
                                                            location = request.data['location'],
                                                            latitude = request.data['latitude'],
                                                            longitude = request.data['longitude'],
                                                            website_link = request.data['website_link'],
                                                            category_id = request.data['category']
                                                            )
                        if resource1 is not None:
                            resource1 = Resources.objects.get(resource_id=resource.resource_id)
                            serializer = ResourcesSerializer(resource1)
                                
                            return Response({"message" : "Updated Successfully", "status" : "1"}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        
                    else:
                        return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                    
                else:
                    return Response({"message" : "Somwthing went wrong", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        print(traceback.format_exc())
        # transaction.rollback()
        return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['POST'])
def delete_resource(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)

                if user is not None:
                    resource = Resources.objects.get(pk=int(request.data['resource_id']));
                    if resource is not None:
                        resource1 = Resources.objects.filter(pk=resource.resource_id).update(status=0)
                        if resource1 is not None:
                            return Response({"message" : "Successfully Deleted", "status" : "1"}, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                    
                else:
                    return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        print(traceback.format_exc())
        return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@csrf_exempt
def add_user_location(request):
    try:
        with transaction.atomic():
            try:
                userLocations = UserLocations.objects.get(
                                            street = request.data['street'],
                                            city = request.data['city'],
                                            ip_address_of_customer = request.data['ip_address_of_customer']
                                                    )
            except:
                userLocations = UserLocations.objects.create(
                                            latitude = request.data['latitude'],
                                            longitude = request.data['longitude'],
                                            street = request.data['street'],
                                            city = request.data['city'],
                                            created_at = datetime.datetime.now(),
                                            ip_address_of_customer = request.data['ip_address_of_customer']
                                                    )
            if userLocations is not None:
                return Response({"message" : "Created Successfully", "status" : "1"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message" : "Something went wrong.", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception:
        print(traceback.format_exc())
        # transaction.rollback()
        return Response({"message" : "Something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from collections import OrderedDict
@api_view(['GET'])
def export_user_locations(request):
    try:
        with transaction.atomic():

            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)

                if user is not None:
                    
                    userLocations = UserLocations.objects.all()
                    userLocationsSerializer = UserLocationsSerializer(userLocations, many = True).data
                    newList = []
                    for r in userLocationsSerializer:    
                        od1 = OrderedDict([
                                ('Location', r['street']),
                                ('City', r['city']),
                                ('IP Address', r['ip_address_of_customer']),
                                ('Time', r['created_at']),
                                ('Latitude', r['latitude']),
                                ('Longitude', r['longitude']),
                            ])
                        
                        newList.append(od1)
                        
                    try:  
                        pathString = str(settings.MEDIA_ROOT) + "/excel/" + str(user.id)
                        
                        for root, dirs, files in os.walk(pathString):
                            for file in files:
                                os.remove(os.path.join(pathString, file))
                        
                        if not os.path.exists(pathString): os.makedirs(pathString)
                        
                        pathUrl = "/user_location_report.xlsx"
                        
                        workbook = xlsxwriter.Workbook(str(pathString) + str(pathUrl))
                        
                        worksheet = workbook.add_worksheet()
                        header1 = 'User Location Report'
                        worksheet.set_header(header1)
                        
                        bold = workbook.add_format({'bold': True, 'align':'center'})
                        headline1 = workbook.add_format({'font_size':11})
                        headline2 = workbook.add_format({'align':'center'})
                        statusColorGreen = workbook.add_format({'font_color': 'green', 'align':'center'}) 
                        statusColorRed = workbook.add_format({'font_color': 'red', 'align':'center'})
                        
                        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'align':'center'})
                        boldHeadline = workbook.add_format({'bold':True, 'align':'center', 'font_size':19})
                        worksheet.set_row(0, 45)  # Set the height of Row 1 to 20.

                        worksheet.merge_range('A1:F1', 'User Location Report', boldHeadline)
                        worksheet.set_column('A:A', 16)
                        worksheet.set_column('B:B', 23)

                        worksheet.set_column('C:D', 17)
                        worksheet.set_column('E:E', 55)
                        worksheet.set_column('F:I', 20)
                        worksheet.set_column('J:J', 66)
                        worksheet.set_column('K:M', 20)
                        worksheet.set_column('N:N', 25)
                        
                        worksheet.set_column('O:P', 36)
                        worksheet.set_column('Q:R', 20)
                        worksheet.set_column('S:S', 40)
                        worksheet.set_column('T:V', 20)

                        worksheet.set_row(1, 18)  # Set the height of Row 1 to 20.
                        worksheet.set_row(2, 18)  # Set the height of Row 1 to 20.
                        
                        
                        rw = 4
                        col = 0
                        amountColumn = 0
                        travellerColumn = 0
                        for r in newList:
                            rw += 1
                            col = 0
                            
                            for key, value in r.items() :
                                worksheet.write(4, col, key, bold)
                                
                                worksheet.write(rw, col, value, headline2)
                                col += 1
                        
                        workbook.close()
                        fileUrl = "media/excel/" + str(user.id) + str(pathUrl)
                        return Response({"message" : "Successfully Done", "status" : "1", "fileUrl":fileUrl}, status=status.HTTP_201_CREATED)
                    
                    except Exception as e1:
                        print(traceback.format_exc())
                        return Response({"message" : str(e1), "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                else:
                    return Response({"message" : "Sorry something went wrong", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : "Sorry something went wrong", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        print(traceback.format_exc())
        return Response({"message" : "Sorry something went wrong", "status" : "0"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)