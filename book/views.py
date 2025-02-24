from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Book
from rest_framework import viewsets
from .serializers import BookSerializer

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book/book_list.html', {'books': books})

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
