from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserRegister
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from .models import UserRegister, Userprofile
from rest_framework import serializers
from .models import Role
from Notification.models import Notification

class RegistrationSerializer(serializers.ModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True, required=False)

    class Meta:
        model = UserRegister
        fields = ('id', 'username', 'password', 'email', 'roles')

    def create(self, validated_data):
        roles = validated_data.pop('roles', [])
        validated_data['password'] = make_password(validated_data['password'])
        user = UserRegister.objects.create(**validated_data)
        
        # Assign roles
        user.roles.set(roles)
        
        # Send notification
        Notification.objects.create(
            user=user,
            message=f"Welcome {user.username}! Your registration is successful."
        )
        return user
    
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegister
        fields = ['id', 'username', 'email', 'name', 'phone', 'address', 'status', 'roles', 'email_confirm', 'phone_confirm', 'create_at', 'create_by', 'update_at', 'update_by', 'notes', 'is_staff']
        read_only_fields = ['create_at', 'update_at', 'create_by', 'update_by']
    
    def create(self, validated_data):
        user = UserRegister.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        print(f"Request data: {data}")

        if username and password:
            try:
                user = UserRegister.objects.get(username=username)
                print(f"User found: {user.username}")
                if check_password(password, user.password):
                    print("Password matches")
                    # Directly authenticate the user
                    user = authenticate(username=username, password=data['password'])
                    if user is None:
                        print("Invalid credentials after authenticate")
                        raise serializers.ValidationError("Invalid credentials username and password work fine.")
                    elif not user.is_active:
                        print("User account is inactive")
                        raise serializers.ValidationError("User account is inactive.")
                else:
                    print("Password does not match")
                    raise serializers.ValidationError("Invalid credentials.")
            except UserRegister.DoesNotExist:
                print("User does not exist")
                raise serializers.ValidationError("Invalid credentials.")
        else:
            print("Must include both username and password")
            raise serializers.ValidationError("Must include both username and password.")
        
        data['user'] = user
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields =('name', 'phone', 'address', 'roles', 'notes')

# ------------------------role management-------------------------------
from rest_framework import serializers
from .models import UserRegister, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserRoleSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True)

    class Meta:
        model = UserRegister
        fields = ['id', 'username', 'roles']

    def update(self, instance, validated_data):
        roles_data = validated_data.pop('roles')
        instance.roles.clear()
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(name=role_data['name'], defaults=role_data)
            instance.roles.add(role)
        instance.save()
        return instance