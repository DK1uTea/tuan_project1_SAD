from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

# Router for API endpoints
router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include API routes
]