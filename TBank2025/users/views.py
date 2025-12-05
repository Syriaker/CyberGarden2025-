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
        summary="Вход или регистрация по никнейму",
        description="Если никнейм существует - возвращает профиль. Если нет - создает новый."
    )
    def post(self, request):
        data = request.data
        nickname = data.get('nickname')

        if not nickname:
            return Response(
                {"error": "Никнейм обязателен!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, created = UserProfile.objects.update_or_create(
            nickname=nickname,
            defaults={
                'current_savings': data.get('current_savings', 0),
                'monthly_savings': data.get('monthly_savings', 0),
                'monthly_spendings': data.get('monthly_spendings', 0),
            }
        )

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