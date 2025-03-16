from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from order.models import Order
from datetime import datetime
from django.utils import timezone

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

@api_view(['POST'])
def api_create_payment(request, order_id):
    """
    Create a new payment for an order
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        
        try:
            order = Order.objects.get(id=order_id, customer=customer)
            
            # Check if payment already exists
            existing_payment = Payment.objects.filter(order=order).first()
            if existing_payment:
                return Response({
                    'error': 'Payment already exists for this order',
                    'payment_id': existing_payment.id,
                    'status': existing_payment.status
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create new payment
            payment = Payment.objects.create(
                order=order,
                amount=order.total_price,
                status='pending'
            )
            
            serializer = PaymentSerializer(payment)
            return Response({
                'message': 'Payment created successfully',
                'payment': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def api_process_payment(request, payment_id):
    """
    Process a payment (simulate payment processing)
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        
        try:
            payment = Payment.objects.get(id=payment_id, order__customer=customer)
            
            # Check if payment is already completed
            if payment.status == 'completed':
                return Response({
                    'error': 'Payment has already been processed',
                    'payment': PaymentSerializer(payment).data
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Simulate payment processing
            payment_method = request.data.get('payment_method', 'credit_card')
            card_number = request.data.get('card_number')
            
            # Simple validation for card number (if provided)
            if payment_method == 'credit_card' and (not card_number or len(str(card_number)) < 13):
                return Response({'error': 'Invalid card number'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Update payment status
            payment.status = 'completed'
            payment.paid_at = timezone.now()
            payment.save()
            
            serializer = PaymentSerializer(payment)
            return Response({
                'message': 'Payment processed successfully',
                'payment': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def api_get_payment_status(request, payment_id=None, order_id=None):
    """
    Get payment status for an order or payment
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        
        try:
            if payment_id:
                # Get payment by ID
                payment = Payment.objects.get(id=payment_id, order__customer=customer)
            elif order_id:
                # Get payment by order ID
                order = Order.objects.get(id=order_id, customer=customer)
                payment = Payment.objects.filter(order=order).first()
                if not payment:
                    return Response({'error': 'No payment found for this order'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Payment ID or Order ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except (Payment.DoesNotExist, Order.DoesNotExist):
            return Response({'error': 'Payment or Order not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def api_get_user_payments(request):
    """
    Get all payments for the current user
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        payments = Payment.objects.filter(order__customer=customer).order_by('-paid_at')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

def payment_page(request, order_id):
    """
    Render the payment page for an order
    """
    return render(request, 'payment/payment_page.html', {'order_id': order_id})

def payment_success(request, payment_id):
    """
    Render payment success page
    """
    return render(request, 'payment/payment_success.html', {'payment_id': payment_id})

