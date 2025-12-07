from django.urls import path
from .views import WishListCreateView, WishDetailView, NotificationListView,ParseItemView

urlpatterns = [
    path('', WishListCreateView.as_view(), name='wish-list-create'),

    path('<int:pk>/', WishDetailView.as_view(), name='wish-detail'),

    path('notifications/', NotificationListView.as_view(), name='notifications-list'),

    path('parse/', ParseItemView.as_view(), name='parse-item'),

]