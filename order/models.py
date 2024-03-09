from django.db import models
from user.models import User
from product.models import Product

# class Cartitem(models.Model):
#     product_name = models.CharField(max_length = 50)
#     quantity = models.IntegerField(default = 1)
#     price = models.IntegerField()
#     customer_name = models.CharField(max_length = 100)
#     def __str__(self):
#         return self.product_name
class Cartitem(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE , related_name = 'cart_item',default = 1)
    quantity = models.IntegerField()
    price = models.IntegerField(default = 500)
    user = models.ForeignKey(User,on_delete=models.CASCADE , related_name = 'cart_item' , default = 1)
    def __str__(self):
        return str(self.product_id)
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default = 1,related_name = 'order_item' )
    created_at = models.DateTimeField(auto_now_add=True )
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE,default = 1,related_name = 'order_item')
    quantity = models.IntegerField(default = 1)
    total_amount = models.IntegerField()

    