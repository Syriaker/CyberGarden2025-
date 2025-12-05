from django.urls import path
from .views import UserAuthView, UserDetailView

urlpatterns = [
    path('login/', UserAuthView.as_view(), name='user-login'),

    path('<str:nickname>/', UserDetailView.as_view(), name='user-detail'),
]