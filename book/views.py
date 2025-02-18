from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Book

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book/book_list.html', {'books': books})
