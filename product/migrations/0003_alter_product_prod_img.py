# Generated by Django 5.0.2 on 2024-02-17 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prod_img',
            field=models.ImageField(blank=True, null=True, upload_to='img'),
        ),
    ]