from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet, add_to_cart, cart, checkout, api_add_to_cart, api_get_cart_items

# Router for API endpoints
router = DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include API routes
    path('add_to_cart/<int:book_id>/', add_to_cart, name='add_to_cart'),  # Add to cart view
    path('cart/', cart, name='cart'),  # Cart view
    path('checkout/', checkout, name='checkout'),  # Checkout view
    path('api/add_to_cart/', api_add_to_cart, name='api_add_to_cart'),  # API endpoint to add to cart
    path('api/get_cart_items/', api_get_cart_items, name='api_get_cart_items'),  # API endpoint to get cart items
]