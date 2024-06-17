from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'content', 'status', 'created', 'modified', 'user_id']