from rest_framework import status
from rest_framework.views import APIView,Response
from django.shortcuts import render,get_object_or_404
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.http import HttpResponse
from django.db.models import Avg
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
User = get_user_model()


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
                        
@api_view(['POST','GET'])
def post_review(request, product_id):
   if request.method=='POST':
      username = request.data.get('username')
      rating = request.data.get('rating')
      review_text = request.data.get('review')
      print(product_id)
      product = get_object_or_404(Product, pk=product_id)
      user = get_object_or_404(User, username=username)

      review = ReviewRating.objects.create(
            product=product,
            user_id=user, 
            review=review_text,
            rating=rating
        )     
      average_rating = ReviewRating.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))['avg_rating'] or rating
      product.average_rating = average_rating
      product.save()

      serializer = ReviewSerializer(review)

      return Response(serializer.data, status=status.HTTP_201_CREATED)
   elif request.method=='GET':
        product = get_object_or_404(Product, pk=product_id)
        reviews = ReviewRating.objects.filter(product=product)
        review_serializer = ReviewSerializer(reviews, many=True)
        average_rating = product.average_rating
        return Response({"Reviews": review_serializer.data, "Average rating": average_rating}, status=status.HTTP_200_OK)
@api_view(['DELETE'])
def delete_review(request):
    review_id=request.data.get('review_id')
    review = get_object_or_404(ReviewRating,id=review_id)
    review.delete()
    return Response({"message": "Review deleted successfully"}, status=status.HTTP_204_NO_CONTENT)   





   
