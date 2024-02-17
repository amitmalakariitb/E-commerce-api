# Generated by Django 5.0.2 on 2024-02-17 18:39

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_prod_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, default=None, null=True)),
            ],
        ),
    ]
