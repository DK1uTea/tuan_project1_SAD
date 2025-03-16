from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (OrderViewSet, OrderItemViewSet, 
                   api_confirm_order, api_get_user_orders, 
                   api_get_order_details, api_cancel_order, 
                   order_history, order_details)

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/confirm_order/', api_confirm_order, name='api_confirm_order'),
    path('api/user_orders/', api_get_user_orders, name='api_get_user_orders'),
    path('api/order_details/<int:order_id>/', api_get_order_details, name='api_get_order_details'),
    path('api/cancel_order/<int:order_id>/', api_cancel_order, name='api_cancel_order'),
    path('history/', order_history, name='order_history'),
    path('details/<int:order_id>/', order_details, name='order_details'),
]