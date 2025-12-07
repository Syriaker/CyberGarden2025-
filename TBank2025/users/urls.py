from django.urls import path
from .views import UserAuthView, UserDetailView

urlpatterns = [
    path('auth/', UserAuthView.as_view(), name='user-auth'),

    path('<str:nickname>/', UserDetailView.as_view(), name='user-detail'),

    path('profile/<str:nickname>/', UserDetailView.as_view(), name='user-detail-profile'),

]