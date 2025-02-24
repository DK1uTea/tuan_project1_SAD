from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from book.models import Book
from customer.models import Customer
from rest_framework import viewsets
from .serializers import CartSerializer, CartItemSerializer

@login_required
def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    customer = request.user.customer  # Assuming a logged-in customer
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    customer = request.user.customer  # Assuming a logged-in customer
    cart = Cart.objects.get(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart/cart.html', {'cart_items': cart_items})

@login_required
def checkout(request):
    customer = request.user.customer  # Assuming a logged-in customer
    cart = Cart.objects.get(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart)
    # Add your checkout logic here
    return render(request, 'cart/checkout.html', {'cart_items': cart_items})

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
