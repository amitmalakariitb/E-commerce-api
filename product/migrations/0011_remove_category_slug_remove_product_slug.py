# Generated by Django 5.0.2 on 2024-03-08 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_remove_product_ratings_product_average_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]
