from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import customer_list, customer_detail, customer_create, customer_update, customer_delete, register, login_view, logout_view, CustomerViewSet, api_register, api_login

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    # Web views
    path('', customer_list, name='customer_list'),  # List customers
    path('<int:customer_id>/', customer_detail, name='customer_detail'),  # Customer detail
    path('create/', customer_create, name='customer_create'),  # Create customer
    path('<int:customer_id>/edit/', customer_update, name='customer_update'),  # Update customer
    path('<int:customer_id>/delete/', customer_delete, name='customer_delete'),  # Delete customer
    path('register/', register, name='register'),  # Register user
    path('login/', login_view, name='login'),  # Login user
    path('logout/', logout_view, name='logout'),  # Logout user

    # API routes
    path('api/', include(router.urls)),  # Include API routes
    path('api/register/', api_register, name='api_register'),  # API endpoint for registration
    path('api/login/', api_login, name='api_login'),  # API endpoint for login
]