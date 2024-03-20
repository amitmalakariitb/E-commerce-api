from rest_framework import serializers
from .models import Cartitem,Order 

class Cart_Item_Serializer(serializers.ModelSerializer):
    # product_id = serializers.IntegerField(source='product.id' , readonly)  # For response only
    # #product_name = serializers.CharField(source='product.product_name', write_only=True , required = True)  # For request and response
    # username = serializers.CharField(source='user.username', required=True)  # For request and response
    # quantity = serializers.IntegerField(default = 1)  # For request and response
    class Meta:
        model = Cartitem
        fields = ['user','quantity','price','product_id']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'quantity' , 'product_id' ,'created_at' , 'total_amount' , 'address']
