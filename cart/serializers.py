from rest_framework import serializers
from .models import Cart, CartItem
from book.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)  # Include book fields

    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'