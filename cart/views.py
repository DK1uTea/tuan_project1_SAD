from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from book.models import Book
from customer.models import Customer
from rest_framework import viewsets
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# View to add a book to the cart, requires user to be logged in
@login_required
def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    customer = request.user.customer  # Assuming a logged-in customer
    cart, created = Cart.objects.get_or_create(customer=customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

# View to display the cart, requires user to be logged in
@login_required
def cart(request):
    customer = request.user.customer  # Assuming a logged-in customer
    cart = Cart.objects.get(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart/cart.html', {'cart_items': cart_items})

# View to handle checkout, requires user to be logged in
@login_required
def checkout(request):
    customer = request.user.customer  # Assuming a logged-in customer
    cart = Cart.objects.get(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart)
    # Add your checkout logic here
    return render(request, 'cart/checkout.html', {'cart_items': cart_items})

# API viewset for Cart model, provides CRUD operations
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

# API viewset for CartItem model, provides CRUD operations
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

# API view to add a book to the cart
@api_view(['POST'])
def api_add_to_cart(request):
    if request.user.is_authenticated:
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'error': 'Book ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        cart_item.quantity += 1
        cart_item.save()
        
        return Response({'message': 'Book added to cart'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

# API view to get cart items
@api_view(['GET'])
def api_get_cart_items(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart = Cart.objects.get(customer=customer)
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
