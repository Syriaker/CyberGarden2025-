from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import WishItem
from users.models import UserProfile
from .serializers import WishItemSerializer
from .services import calculate_cooling_data


class WishListCreateView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='X-User-Nickname',
                type=str,
                location=OpenApiParameter.HEADER,
                description='Никнейм пользователя',
                required=True
            )
        ],
        responses={200: WishItemSerializer(many=True)},
        summary="Получить список желаний"
    )
    def get(self, request):
        nickname = request.headers.get('X-User-Nickname')
        if not nickname:
            return Response({"error": "Header X-User-Nickname is required"}, status=400)

        wishes = WishItem.objects.filter(user__nickname=nickname)
        serializer = WishItemSerializer(wishes, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='X-User-Nickname',
                type=str,
                location=OpenApiParameter.HEADER,
                description='Никнейм пользователя',
                required=True
            )
        ],
        request=WishItemSerializer,
        responses={201: WishItemSerializer},
        summary="Добавить желание"
    )
    def post(self, request):
        nickname = request.headers.get('X-User-Nickname')
        if not nickname:
            return Response({"error": "Header X-User-Nickname is required"}, status=400)

        try:
            user = UserProfile.objects.get(nickname=nickname)
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        serializer = WishItemSerializer(data=request.data)
        if serializer.is_valid():
            price = serializer.validated_data.get('price')

            end_date, final_days, details, notifications = calculate_cooling_data(price, user)

            wish = serializer.save(user=user, cooling_end_date=end_date)

            response_data = serializer.data
            response_data['calculation_info'] = details
            response_data['notification_plan'] = notifications

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishDetailView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='X-User-Nickname',
                type=str,
                location=OpenApiParameter.HEADER,
                required=True
            )
        ],
        summary="Удалить желание"
    )
    def delete(self, request, pk):
        nickname = request.headers.get('X-User-Nickname')
        if not nickname:
            return Response({"error": "Header X-User-Nickname is required"}, status=400)

        wish = get_object_or_404(WishItem, pk=pk, user__nickname=nickname)

        wish.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)