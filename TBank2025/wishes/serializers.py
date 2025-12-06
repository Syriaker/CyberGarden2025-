from rest_framework import serializers
from .models import WishItem
from users.models import UserProfile


class WishItemSerializer(serializers.ModelSerializer):

    days_left = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = WishItem
        fields = [
            'id', 'title', 'price', 'category',
            'status', 'status_display', 'created_at', 'cooling_end_date', 'days_left'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'cooling_end_date','days_left']

    def get_days_left(self, obj):
        from django.utils import timezone
        if not obj.cooling_end_date:
            return 0
        delta = obj.cooling_end_date - timezone.now()
        return max(delta.days, 0)
