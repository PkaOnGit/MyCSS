from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from django.contrib.auth import authenticate,login
from .serializers import RegistrationSerializer
from .models import UserRegister
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class LoginAPIView(APIView):

    def get(self, request):
        # Handle GET request (if needed)
        return Response({"detail": "GET request received"}, status=status.HTTP_200_OK)

    def post(self, request):
        print("Request data:", request.data)  # Print request data for debugging
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)  # Log the user in
                print("Login successful")  # Print login success message for debugging
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                print("Invalid credentials")  # Print invalid credentials message for debugging
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            print("Validation errors:", serializer.errors)  # Print validation errors for debugging
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPIView(APIView):

    def get(self, request):
        # Handle GET request (if needed)
        return Response({"detail": "GET request received"}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteUserAPIView(APIView):

    def delete(self, request, user_id):
        try:
            user = UserRegister.objects.get(id=user_id)
            user.delete()
            return Response({'detail': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except UserRegister.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)