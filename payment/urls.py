from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentViewSet, api_create_payment, api_process_payment, 
    api_get_payment_status, api_get_user_payments,
    payment_page, payment_success
)

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/create_payment/<int:order_id>/', api_create_payment, name='api_create_payment'),
    path('api/process_payment/<int:payment_id>/', api_process_payment, name='api_process_payment'),
    path('api/payment_status/<int:order_id>/', api_get_payment_status, name='api_get_payment_status'),
    path('api/user_payments/', api_get_user_payments, name='api_get_user_payments'),
    path('payment/<int:order_id>/', payment_page, name='payment_page'),
    path('success/<int:payment_id>/', payment_success, name='payment_success'),
]