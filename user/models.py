from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=10)
    username = models.CharField(null = True ,unique = True, blank = True , max_length = 25)
    def __str__(self):
        return self.username

class Address(models.Model):
    door_no = models.CharField(max_length = 10 , null = True)
    street = models.CharField(max_length=120, null = True)
    city = models.CharField(max_length=25, null = True)
    state = models.CharField(max_length=25, null = True)
    pincode = models.CharField(max_length=6, null = True)
    user = models.ForeignKey(User, related_name='addresses' , on_delete=models.CASCADE)

class primeuser(models.Model):
    user = models.ForeignKey(User, related_name='primeuser' , on_delete=models.CASCADE)
    is_prime_user = models.BooleanField(default = False)
    otp = models.CharField(max_length =  6 )
