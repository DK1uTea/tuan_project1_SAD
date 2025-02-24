"""
URL configuration for tuan_project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from book.views import BookViewSet
from cart.views import CartViewSet, CartItemViewSet
from customer.views import CustomerViewSet
from book.views import book_list
from cart.views import add_to_cart, cart, checkout
from django.contrib.auth.views import LoginView

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='customer/login.html'), name='login'),
    path('register/', include('customer.urls')),
    path('customers/', include('customer.urls')),
    path('add_to_cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('', book_list, name='book_list'),
    path('api/', include(router.urls)),  # Thêm dòng này
]
