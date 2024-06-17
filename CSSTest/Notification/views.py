from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer

class ListNotificationsAPIView(APIView):
    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)