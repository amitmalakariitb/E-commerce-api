from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password' , 'mobile_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        mobile_number = validated_data.pop('mobile_number',None)
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        if mobile_number:
            user.mobile_number = mobile_number
        else:
            raise serializers.ValidationError("Mobile number is required")
        user.set_password(validated_data['password'])
        user.save()
        return user