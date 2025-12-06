from django.urls import path
from .views import WishListCreateView

urlpatterns = [
    path('', WishListCreateView.as_view(), name='wish-list-create'),
]