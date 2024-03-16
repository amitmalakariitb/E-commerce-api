from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import Cart_Item_Serializer , OrderItemSerializer
from .models import Cartitem , Order 
from product.models import Product
from user.models import primeuser , User
from django.contrib.auth import get_user_model
User = get_user_model()
@api_view(['POST'])
def add_to_cart(request):
    #request data will contain only product name , quantity , user details . We need to find it's price by generating product_id for that product 
    #and from that product id we will get it's price
    if request.method == 'POST':
        try:
           product = Product.objects.get(id=request.data.get('product_id'))
        except Product.DoesNotExist:
            return Response({"error": "Product does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart_item = Cartitem.objects.get(product_id=request.data.get('product_id'), user_id=request.data.get('user'))
            # If the product exists, increase the quantity
            q = int(cart_item.quantity)
            k = int(cart_item.price)
            cart_item.quantity += int(request.data.get('quantity'))
            cart_item.price += (k/q)*int(request.data.get('quantity'))
            cart_item.save()
            return Response({"message": "Quantity updated in the cart.", "data": Cart_Item_Serializer(cart_item).data}, status=status.HTTP_200_OK)
        except Cartitem.DoesNotExist:
            pass
        try:
            prime_user = primeuser.objects.get(user_id=request.data.get('user'))
            name = User.objects.get(id = request.data.get('user'))
            username = name.username
            q = int(request.data.get('quantity'))
            request.data['price'] = (product.price)*(q)*0.8
            serializer = Cart_Item_Serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": f"{username} is a prime user so there is a discount of 20% on each product", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except primeuser.DoesNotExist:
            pass
        q = int(request.data.get('quantity'))
        request.data['price'] = (product.price)*(q)
        serializer = Cart_Item_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_cart(request , pk):
    if request.method == 'GET':
        cart_items = Cartitem.objects.filter(user_id= pk)
        serializer = Cart_Item_Serializer(cart_items, many=True)
        modified_serializer_data = []
        for item in serializer.data:
            product_id = item.get('product_id')
            user_id = pk
            product = Product.objects.get(id=product_id)
            item['product_name'] = product.prod_name
            item['brand_name'] = product.brand
            item['product_image'] = product.prod_img.url if product.prod_img else None
            item['description'] = product.description
            item['average_rating'] = product.average_rating
            item['category'] = product.category.title if product.category else None
            cart_items = Cartitem.objects.filter(user_id=user_id, product_id=product_id)
            if cart_items.exists():
                cart_item = cart_items.first()
                cart_item_id = cart_item.id
                item['primary key or cart_item_id'] = cart_item_id
            # Add more modifications as needed
            modified_serializer_data.append(item)
        
        # Merge modified serializer data with additional data
        response_data = {
            'cart_items': modified_serializer_data,
        }
        return Response(response_data)

@api_view(['PATCH' , 'PUT' , 'DELETE'])
def edit_cart(request ,pk):#pk stands for primary key
    try:
        cart_item = Cartitem.objects.get(pk=pk)
    except Cartitem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH' or request.method == 'PUT':
        q = int(request.data.get('quantity'))
        if q == 0:
            cart_item.delete()
            return Response({"message":"Deleted successfully"})
        else:
            productid = int(cart_item.product_id_id)
            userid = int(cart_item.user_id)
            Price = int(cart_item.price)
            Q = int(cart_item.quantity)
            request.data['price'] = (Price/Q)*(q)
            request.data['user'] = userid
            request.data['product_id'] = productid
            serializer = Cart_Item_Serializer(cart_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    elif request.method == 'DELETE': 
        cart_item.delete()
        return Response({"message":"Deleted successfully"},status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def direct_purchase(request):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=request.data.get('product_id'))
        except Product.DoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
        q = int(request.data.get('quantity'))
        try:
            prime_user = primeuser.objects.get(user_id=request.data.get('user'))
            name = User.objects.get(id = request.data.get('user'))
            username = name.username
            request.data['total_amount'] = (product.price)*(q)*(0.8)
            serializer = OrderItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({username: "is  a prime user so there is a discount of 20'%' on the final amount " ,"message": "Order placed successfully" , "data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except primeuser.DoesNotExist:
            pass
        request.data['total_amount'] = (product.price)*(q)
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order placed successfully" , "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def checkout(request):
    if request.method == 'POST':
        cart_items = Cartitem.objects.filter(user_id=request.data.get('user'))
        total_amount = sum(item.price * item.quantity for item in cart_items)
        if cart_items:
            for cart_item in cart_items:
                serializer = OrderItemSerializer(data = cart_item)
                if serializer.is_valid():
                    serializer.save()
                cart_item.delete()
            return Response({"message": "Order placed successfully" , "Total_amount":total_amount},status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)   