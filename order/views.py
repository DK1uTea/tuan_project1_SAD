from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cart.models import Cart, CartItem
from decimal import Decimal

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

@api_view(['POST'])
def api_confirm_order(request):
    """
    Create a new order from the user's cart items
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        cart = Cart.objects.get(customer=customer)
        cart_items = CartItem.objects.filter(cart=cart)
        
        # Calculate total price
        total_price = sum(item.quantity * item.book.price for item in cart_items)
        
        # Create order
        order = Order.objects.create(
            customer=customer,
            total_price=total_price
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                cart_item=cart_item,
                quantity=cart_item.quantity
            )
        
        # Clear the cart after creating the order
        cart_items.delete()
        
        return Response({
            'message': 'Order created successfully',
            'order_id': order.id
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def api_get_user_orders(request):
    """
    Get all orders for the current user
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def api_get_order_details(request, order_id):
    """
    Get details for a specific order
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        try:
            order = Order.objects.get(id=order_id, customer=customer)
            order_serializer = OrderSerializer(order)
            order_items = OrderItem.objects.filter(order=order)
            item_serializer = OrderItemSerializer(order_items, many=True)
            
            response_data = {
                'order': order_serializer.data,
                'items': item_serializer.data
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
def api_cancel_order(request, order_id):
    """
    Cancel a specific order
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        try:
            order = Order.objects.get(id=order_id, customer=customer)
            # Check if order can be canceled (you might want to add more checks)
            order.delete()
            return Response({'message': 'Order canceled successfully'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

def order_history(request):
    return render(request, 'order/order_history.html')

def order_details(request, order_id):
    return render(request, 'order/order_details.html', {'order_id': order_id})
