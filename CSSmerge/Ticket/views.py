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

User = get_user_model()

class TicketCreateAPIView(APIView):
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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketEditAPIView(APIView):
    def get(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({'detail': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            serializer = TicketSerializer(ticket, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Ticket.DoesNotExist:
            return Response({'detail': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
        
class ListTicketsAPIView(APIView):
    def get(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)