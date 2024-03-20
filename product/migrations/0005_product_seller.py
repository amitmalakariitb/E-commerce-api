# Generated by Django 5.0.2 on 2024-03-19 10:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.seller'),
        ),
    ]