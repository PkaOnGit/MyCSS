from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer
from .models import UserRegister 
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserRegister
from .serializers import UserRegisterSerializer, RegistrationSerializer, LoginSerializer
from Notification.models import Notification
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .permissions import RolePermissionFactory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserRegister, Role

User = get_user_model()

class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            roles = validated_data.pop('roles', [])

            # Validate the password
            password = validated_data.get('password')
            user = UserRegister(**validated_data)  # Create an instance without saving to pass to the validator
            try:
                validate_password(password, user=user)
            except DjangoValidationError as e:
                return Response({
                    "status": "error",
                    "status_code": 400,
                    "message": "User registration unsuccessful",
                    "errors": {'password': list(e.messages)}
                }, status=status.HTTP_400_BAD_REQUEST)

            validated_data['password'] = make_password(password)
            user.save()  # Now save the instance

            # Assign roles
            user.roles.set(roles)

            # Send notification
            Notification.objects.create(
                user=user,
                message=f"Welcome {user.username}! Your registration is successful."
            )

            # Send email notification
            send_mail(
                'Registration Successful',
                f'Welcome {user.username}! Your registration is successful.',
                'from@example.com',  # Replace with your sender email
                [user.email],
                fail_silently=False,
            )

            # Format and return the response
            response_data = {
                "status": "success",
                "status_code": 201,
                "message": "User registration successful",
                "user": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(
            {
                "status": "error",
                "status_code": 400,
                "message": "User registration unsuccessful",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class UserProfileAPIView(APIView):
    permission_classes = [RolePermissionFactory('Admin', 'Staff')]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserRegisterSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserRegisterSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                Notification.objects.create(
                    user=user,
                    message="Your profile has been updated by the admin."
                )
                # Send email notification
                send_mail(
                    'Profile Updated',
                    'Your profile has been updated by the admin.',
                    'from@example.com',  # Replace with your sender email
                    [user.email],
                    fail_silently=False,
                )
                response_data = {
                    "status": "success",
                    "status_code": 200,
                    "message": "Profile updated successfully",
                    "user": serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            response_data = {
                "status": "error",
                "status_code": 400,
                "message": "Profile update failed",
                "errors": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            response_data = {
                "status": "error",
                "status_code": 404,
                "message": "User not found"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({
                "status": "success",
                "status_code": 200,
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "error",
                "status_code": 400,
                "message": "Login unsuccessful",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class ListUsersAPIView(APIView):
    permission_classes = [RolePermissionFactory('Admin', 'Staff')]
    
    def get(self, request):
        users = UserRegister.objects.all()
        serializer = RegistrationSerializer(users, many=True)
        return Response(serializer.data)
    
# -------------role management-------------
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Role, UserRegister
from .serializers import RoleSerializer, UserRoleSerializer

class RoleListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [RolePermissionFactory('Admin', 'Staff')]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class UserRoleAPIView(APIView):
    permission_classes = [RolePermissionFactory('Admin', 'Staff')]

    def get(self, request, user_id):
        try:
            user = UserRegister.objects.get(id=user_id)
            serializer = UserRoleSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserRegister.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        try:
            user = UserRegister.objects.get(id=user_id)
            serializer = UserRoleSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                Notification.objects.create(
                    user=user,
                    message="Your profile has been updated by the admin."
                )
                # Send email notification
                send_mail(
                    'Role updating',
                    'Your role has been update.',
                    'phakkapol@e-works.co.uk',
                    [user.email],
                    fail_silently=False,
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserRegister.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)