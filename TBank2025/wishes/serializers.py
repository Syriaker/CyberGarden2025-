from rest_framework import serializers
from .models import WishItem, Notification
from django.utils import timezone

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']

class WishItemSerializer(serializers.ModelSerializer):
    days_left = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = WishItem
        fields = [
            'id', 'title', 'price', 'category','status',
            'status_display', 'created_at', 'cooling_end_date', 'days_left',
            'notify_on_end', 'report_frequency','image_url'
        ]
        read_only_fields = ['id', 'created_at', 'cooling_end_date', 'days_left']

    def get_days_left(self, obj):
        if not obj.cooling_end_date:
            return 0
        delta = obj.cooling_end_date - timezone.now()
        return max(delta.days, 0)