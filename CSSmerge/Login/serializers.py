from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserRegister
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from .models import UserRegister

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegister
        fields = '__all__'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = UserRegister.objects.create(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = make_password(data.get('password'))

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Must include both username and password.")
        
        data['user'] = user
        return data