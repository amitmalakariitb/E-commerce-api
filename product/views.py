from rest_framework import status
from rest_framework.views import APIView,Response
from django.shortcuts import render,get_object_or_404
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *




@api_view(['GET','POST'])
def api_products(request):
    if request.method=='GET':
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)
    if request.method=='POST':
       serializer=ProductSerializer(data=request.data)
       if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)


@api_view()
def api_product(request,pk):
   product=get_object_or_404(Product,id =pk)
   serializer=ProductSerializer(product)
   return Response(serializer.data)

@api_view(['GET','POST'])
def api_categories(request):
    if request.method=='GET':
        categories=Category.objects.all()
        serializer=CategorySerializer(categories,many=True)
        return Response(serializer.data)
    if request.method=='POST':
       serializer=CategorySerializer(data=request.data)
       if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)



@api_view()
def api_category(request,pk):
  category=get_object_or_404(Category , category_id =pk)
  serializer=CategorySerializer(category)
  return Response(serializer.data)
                        