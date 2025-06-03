from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'notification_type', 'created_at', 'url']
        read_only_fields = ['user', 'created_at']