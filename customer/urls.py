from django.urls import path
from .views import customer_list, customer_detail, customer_create, customer_update, customer_delete, register, login_view, logout_view

urlpatterns = [
    path('', customer_list, name='customer_list'),
    path('<int:customer_id>/', customer_detail, name='customer_detail'),
    path('create/', customer_create, name='customer_create'),
    path('<int:customer_id>/edit/', customer_update, name='customer_update'),
    path('<int:customer_id>/delete/', customer_delete, name='customer_delete'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]