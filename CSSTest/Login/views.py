from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, UserProfileSerializer
from .models import UserRegister 
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserRegister
from .serializers import UserRegisterSerializer, RegistrationSerializer
from Notification.models import Notification
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .permissions import RolePermissionFactory

User = get_user_model()

class RegisterUserAPIView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Notification.objects.create(user=user, message="Welcome to the system!")
            # Send email notification
            send_mail(
                'Welcome to the system',
                'Thank you for registering.',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = UserRegister.objects.get(username=username)
            if check_password(password, user.password):
                return Response({'detail': 'Login successful', 'id': user.id}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except UserRegister.DoesNotExist:
            return Response({'detail': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

# class DeleteUserAPIView(APIView):
    
#     def delete(self, request, user_id):
#         try:
#             user = UserRegister.objects.get(id=user_id)
#             user.delete()
#             return Response({'detail': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#         except UserRegister.DoesNotExist:
#             return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# class CustomAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'id': user.id,
#             'username': user.username
#         })
    
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
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserRegister.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)