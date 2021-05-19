from django.contrib.auth.models import User

from rest_framework import serializers

from resources.models import *

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('category_id', 'category_name', 'status')

class ResourcesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resources
        fields = ('resource_id', 'resource_name', 'eligibility', 'resource_description', 'office_hours', 'phone', 'location', 'latitude', 'longitude', 'website_link', 'category', 'status')
        
class UserLocationsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserLocations
        fields = ('id', 'latitude', 'longitude', 'street', 'city', 'created_at')