from django.urls import path
from .views import WishListCreateView, WishDetailView

urlpatterns = [
    path('', WishListCreateView.as_view(), name='wish-list-create'),

    path('<int:pk>/', WishDetailView.as_view(), name='wish-detail'),
]