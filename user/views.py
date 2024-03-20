from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer , AddressSerializer , PrimeuserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from .models import User , Address , primeuser
import random

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            Userid = User.objects.get(username = username)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key , "user_id":Userid.pk}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view([ 'POST'])
def add_new_address(request):
    if request.method == 'POST':
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            door_no = serializer.validated_data.get('door_no')
            street = serializer.validated_data.get('street')
            city = serializer.validated_data.get('city')
            state = serializer.validated_data.get('state')
            pincode = serializer.validated_data.get('pincode')
            user = serializer.validated_data.get('user')
            existing_address = Address.objects.filter(
                door_no = door_no,
                street=street,
                city=city,
                state=state,
                pincode=pincode,
                user_id = user).exists()
        if existing_address:
            return Response({"message": "Address already exists"},  status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"message": "Address saved successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
@api_view(['GET'])
def view_saved_addresses(request , pk):  
    if request.method == 'GET': 
        address = Address.objects.filter(user_id=pk)
        if address:
            serializer = AddressSerializer(address, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "No saved addresses found for the user."},  status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT','PATCH','DELETE'])
def edit_saved_addresses(request , pk):
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "PUT" or request.method == "PATCH":
        serializer =  AddressSerializer(address , data = request.data)   
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE': 
        address.delete()
        return Response({"message":"Address deleted successfully"},status=status.HTTP_204_NO_CONTENT)

  
@api_view(['POST', 'GET'])
def prime_user(request):
    if request.method == 'GET':
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        OTP = otp
        return Response({"message": "Your OTP is", "otp": otp}, status=status.HTTP_201_CREATED)

    elif request.method == 'POST':
        OTp = request.data.get('otp')
        OTP = 556677  # Using the get method we can get an OTP value at each and every time we use that. Enter that value here and the prime user will be created.
        if len(OTp) == 6:
            if int(OTp) == OTP:
                try:
                    prime_user = primeuser.objects.get(user_id=request.data.get('user'))
                    name = User.objects.get(id = request.data.get('user'))
                    username = name.username
                    return Response({username: "is already a prime user" }, status=status.HTTP_400_BAD_REQUEST)
                except primeuser.DoesNotExist:
                    pass
                request.data['is_prime_user'] = True
                serializer = PrimeuserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Prime user created"}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "OTP should have six digits"}, status=status.HTTP_400_BAD_REQUEST)
            