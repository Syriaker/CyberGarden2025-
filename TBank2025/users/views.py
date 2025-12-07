from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import UserProfile
from .serializers import UserProfileSerializer
from decimal import Decimal


class UserAuthView(APIView):

    @extend_schema(
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer},
        summary="Вход или регистрация по никнейму"
    )
    def post(self, request):
        data = request.data
        nickname = data.get('nickname')
        if not nickname:
            return Response({"error": "No nickname"}, status=400)

        def get_decimal(val):
            if val is None or val == "": return 0
            return Decimal(str(val))

        user, created = UserProfile.objects.get_or_create(nickname=nickname)

        if 'email' in data:
            user.email = data['email']

        if 'theme' in data:
            user.theme = data['theme']

        forbidden = data.get('forbidden_categories')
        if forbidden is not None and isinstance(forbidden, list):
            user.blacklisted_categories = ", ".join(forbidden)

        new_cur = get_decimal(data.get('current_savings'))
        new_save = get_decimal(data.get('monthly_savings'))
        new_spend = get_decimal(data.get('monthly_spendings'))

        if created or new_cur > 0: user.current_savings = new_cur
        if created or new_save > 0: user.monthly_savings = new_save
        if created or new_spend > 0: user.monthly_spendings = new_spend

        user.save()

        serializer = UserProfileSerializer(user)
        return Response({
            "status": "created" if created else "updated",
            "data": serializer.data
        })


class UserDetailView(APIView):

    @extend_schema(
        responses={200: UserProfileSerializer},
        summary="Получить профиль пользователя"
    )
    def get(self, request, nickname):
        try:
            user = UserProfile.objects.get(nickname=nickname)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND
            )