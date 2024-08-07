from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ticket
from .serializers import TicketSerializer
from django.contrib.auth import get_user_model
from Notification.models import Notification
from Login.models import UserRegister
from django.core.mail import send_mail
import logging
from Login.permissions import RolePermissionFactory
from django.conf import settings


User = get_user_model()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TicketCreateAPIView(APIView):
    # permission_classes = [RolePermissionFactory('Admin', 'Staff', 'User')]

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id')
            try:
                user = User.objects.get(id=user_id)
                ticket = serializer.save(user=user)
                Notification.objects.create(user=user, message="Your ticket has been created!")
                # Send email notification
                send_mail(
                    'Ticket Created',
                    f'Thank you for creating a ticket: {ticket.title}',
                    'from@example.com',
                    [user.email],
                    fail_silently=False,
                )
                response_data = {
                    "status": "success",
                    "status_code": 201,
                    "message": "Ticket created successfully",
                    "ticket": serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                response_data = {
                    "status": "error",
                    "status_code": 400,
                    "message": "User does not exist"
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        response_data = {
            "status": "error",
            "status_code": 400,
            "message": "Ticket creation failed",
            "errors": serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class TicketEditAPIView(APIView):
    permission_classes = [RolePermissionFactory('Admin', 'Staff')]

    def get(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({'detail': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, ticket_id):
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            ticket = Ticket.objects.get(id=ticket_id)
            user = User.objects.get(id=user_id)
            serializer = TicketSerializer(ticket, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                Notification.objects.create(
                    user=ticket.user,
                    message="Your ticket has been updated by the admin."
                )
                send_mail(
                    'Ticket Updated',
                    f'Thank you for updating the ticket: {ticket.title}',
                    'your-email@example.com',  # Ensure this matches EMAIL_HOST_USER
                    [user.email],
                    fail_silently=False,
                )
                response_data = {
                    "status": "success",
                    "status_code": 200,
                    "message": "Ticket updated successfully",
                    "ticket": serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            response_data = {
                "status": "error",
                "status_code": 400,
                "message": "Ticket update failed",
                "errors": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except (Ticket.DoesNotExist, User.DoesNotExist):
            response_data = {
                "status": "error",
                "status_code": 404,
                "message": "Ticket or user not found"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
class ListTicketsAPIView(APIView):
    permission_classes = [RolePermissionFactory('Admin', 'Staff')]
    
    def get(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)