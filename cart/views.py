from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from book.models import Book
from customer.models import Customer

@login_required
def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    customer = Customer.objects.first()  # Assuming a logged-in customer
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    customer = Customer.objects.first()  # Assuming a logged-in customer
    cart = Cart.objects.get(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart/cart.html', {'cart_items': cart_items})
