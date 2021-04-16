from django.db import models

# Create your models here.


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255, default= None)
    status = models.IntegerField(default=1)

    def __str__(self):
        return str(self.category_name)

class Resources(models.Model):
    resource_id = models.AutoField(primary_key=True)
    resource_name = models.CharField(max_length=255, default= None)
    eligibility = models.CharField(max_length=500, default=None)
    resource_description = models.CharField(max_length=1000, default=None)
    office_hours = models.CharField(max_length=255, default= None)
    phone = models.CharField(max_length=255, default= None)
    location = models.CharField(max_length=255, default= None)
    latitude = models.FloatField(default= 0)
    longitude = models.FloatField(default= 0)
    website_link = models.URLField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    status = models.IntegerField(default=1)

    def __str__(self):
        return str(self.resource_name)
