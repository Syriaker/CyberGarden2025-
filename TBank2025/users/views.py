from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import UserProfile
from .serializers import UserProfileSerializer


class UserAuthView(APIView):

    @extend_schema(
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer},
        summary="Вход или регистрация по никнейму"
    )
    def post(self, request):
        print("ПРИШЛО С ФРОНТА:", request.data)
        data = request.data
        nickname = data.get('nickname')

        if not nickname:
            return Response(
                {"error": "Никнейм обязателен!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        def get_value(key):
            val = data.get(key)
            if val is None or val == "":
                return 0
            return float(val)

        new_savings = get_value('current_savings')
        new_monthly_save = get_value('monthly_savings')
        new_monthly_spend = get_value('monthly_spendings')

        user, created = UserProfile.objects.get_or_create(nickname=nickname)

        if created:
            user.current_savings = new_savings
            user.monthly_savings = new_monthly_save
            user.monthly_spendings = new_monthly_spend
            user.save()
        else:

            data_changed = False

            if new_savings > 0:
                user.current_savings = new_savings
                data_changed = True

            if new_monthly_save > 0:
                user.monthly_savings = new_monthly_save
                data_changed = True

            if new_monthly_spend > 0:
                user.monthly_spendings = new_monthly_spend
                data_changed = True

            if data_changed:
                user.save()

        serializer = UserProfileSerializer(user)

        return Response({
            "status": "created" if created else "logged_in",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


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