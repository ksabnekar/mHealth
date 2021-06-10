# Generated by Django 3.1.7 on 2021-06-10 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(default=None, max_length=255)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserLocations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('latitude', models.CharField(default=None, max_length=255)),
                ('longitude', models.CharField(default=None, max_length=500)),
                ('street', models.CharField(default=None, max_length=1000)),
                ('city', models.CharField(default=None, max_length=255)),
                ('created_at', models.DateTimeField(null=True)),
                ('ip_address_of_customer', models.CharField(default=None, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('resource_id', models.AutoField(primary_key=True, serialize=False)),
                ('resource_name', models.CharField(default=None, max_length=255)),
                ('eligibility', models.CharField(default=None, max_length=500)),
                ('resource_description', models.CharField(default=None, max_length=1000)),
                ('office_hours', models.CharField(default=None, max_length=255)),
                ('phone', models.CharField(default=None, max_length=255)),
                ('location', models.CharField(default=None, max_length=255)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
                ('website_link', models.URLField()),
                ('status', models.IntegerField(default=1)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='resources.category')),
            ],
        ),
    ]
