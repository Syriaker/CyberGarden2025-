from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import WishItem
from users.models import UserProfile
from .serializers import WishItemSerializer
from .services import calculate_cooling_data


class WishListCreateView(APIView):
    @extend_schema(
        parameters=[
            {'name': 'nickname', 'in': 'query', 'description': 'Никнейм пользователя', 'required': True,
             'type': 'string'}
        ],
        responses={200: WishItemSerializer(many=True)},
        summary="Получить список желаний"
    )
    def get(self, request):
        nickname = request.query_params.get('nickname')
        if not nickname:
            return Response({"error": "Укажите ?nickname=..."}, status=400)

        wishes = WishItem.objects.filter(user__nickname=nickname)
        serializer = WishItemSerializer(wishes, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=WishItemSerializer,
        responses={201: WishItemSerializer},
        summary="Добавить желание и рассчитать сложный срок"
    )
    def post(self, request):
        serializer = WishItemSerializer(data=request.data)
        if serializer.is_valid():
            nickname = serializer.validated_data.get('nickname')
            price = serializer.validated_data.get('price')

            try:
                user = UserProfile.objects.get(nickname=nickname)
            except UserProfile.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

            end_date, final_days, details, notifications = calculate_cooling_data(price, user)

            wish = serializer.save(cooling_end_date=end_date)

            response_data = serializer.data
            response_data['calculation_info'] = details
            response_data['notification_plan'] = notifications

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)