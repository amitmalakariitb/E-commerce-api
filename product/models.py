from django.db import models
import uuid

# Create your models here.
class Category(models.Model):
    category_id=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,unique=True)
    title=models.TextField(blank=True,null=True)
    slug=models.SlugField(default=None,null=True,blank=True)


class Product(models.Model):
    prod_name=models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=None,null=True,blank=True)
    brand=models.CharField(max_length=100, blank=True,null=True)
    price=models.FloatField(default=500.0)
    prod_img=models.ImageField(upload_to='img',blank=True,null=True)
    description=models.TextField(blank=True ,null=True)
    ratings=models.FloatField(null=True,blank=True)
    slug=models.SlugField(default=None,null=True,blank=True)




