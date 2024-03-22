from django.db import models
import uuid
from user.models import *
from django.db.models import Avg


# Create your models here.
class Category(models.Model):
    category_id=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,unique=True)
    title=models.TextField(blank=True,null=True)

class Seller(models.Model):
    name=models.TextField(max_length=100,blank=True,null=True)
    email = models.EmailField(unique=True,blank=True,null=True)
    mobile_number = models.CharField(max_length=10,blank=True,null=True)
    address = models.CharField(max_length=400,blank=True,null=True)
    license_no = models.CharField(max_length=100,blank=True,null=True)


class Product(models.Model):
    prod_name=models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,default=None,null=True,blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=None, null=True, blank=True)
    brand=models.CharField(max_length=100, blank=True,null=True)
    price=models.FloatField(default=500.0)
    prod_img=models.ImageField(upload_to='img',blank=True,null=True)
    description=models.TextField(blank=True ,null=True)
    average_rating=models.FloatField(null=True, blank=True, default=0)
    is_out_of_stock=models.BooleanField(null=True, blank=True,default=False)



class ReviewRating(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,default=None,null=True,blank=True)
    user_id=models.ForeignKey(User ,on_delete=models.SET_NULL,default=None,null=True,blank=True)
    review=models.CharField(max_length=400,default='Default review text')
    rating=models.FloatField()
    class Meta:
        unique_together = ('product', 'user_id')


