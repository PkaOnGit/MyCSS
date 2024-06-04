from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from django.contrib.auth import authenticate,login
from .serializers import RegisterSerializer

class LoginAPIView(APIView):

    def get(self, request):
        # Handle GET request (if needed)
        return Response({"detail": "GET request received"}, status=status.HTTP_200_OK)

    def post(self, request):
        print("Request data:", request.data)  # Print request data for debugging
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=email, password=password)
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
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)