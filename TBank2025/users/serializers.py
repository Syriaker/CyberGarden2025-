from rest_framework import serializers
from .models import UserProfile
from decimal import Decimal


class UserProfileSerializer(serializers.ModelSerializer):
    availableCash = serializers.SerializerMethodField(method_name='get_available_cash')

    forbidden_categories = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'nickname', 'email', 'theme',
            'current_savings', 'monthly_savings', 'monthly_spendings',
            'availableCash', 'forbidden_categories'
        ]

    def get_available_cash(self, obj):
        if not obj.current_savings: return 0.0
        return float(Decimal(str(obj.current_savings)) * Decimal('0.5'))

    def get_forbidden_categories(self, obj):
        if not obj.blacklisted_categories:
            return []
        return [x.strip() for x in obj.blacklisted_categories.split(',') if x.strip()]

