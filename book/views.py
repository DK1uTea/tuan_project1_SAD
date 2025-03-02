from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Book
from rest_framework import viewsets
from .serializers import BookSerializer

# View to display the list of books, requires user to be logged in
@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book/book_list.html', {'books': books})

# API viewset for Book model, provides CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
