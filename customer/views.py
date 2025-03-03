from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Customer
from .forms import UserRegistrationForm, CustomerForm
from rest_framework import viewsets
from .serializers import CustomerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

# View to display the list of customers
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer/customer_list.html', {'customers': customers})

# View to display the details of a specific customer
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, 'customer/customer_detail.html', {'customer': customer})

# View to create a new customer
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customer/customer_form.html', {'form': form})

# View to update an existing customer
def customer_update(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', customer_id=customer.id)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer/customer_form.html', {'form': form})

# View to delete a customer
def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customer/customer_confirm_delete.html', {'customer': customer})

# View to handle user registration
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        customer_form = CustomerForm()
    return render(request, 'customer/register.html', {'user_form': user_form, 'customer_form': customer_form})

# View to handle user login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('book_list')
        else:
            return render(request, 'customer/login.html', {'error': 'Invalid credentials'})
    return render(request, 'customer/login.html')

# View to handle user logout
def logout_view(request):
    logout(request)
    return redirect('login')

# API viewset for Customer model, provides CRUD operations
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

@api_view(['POST'])
def api_register(request):
    user_form = UserRegistrationForm(request.data)
    customer_form = CustomerForm(request.data)
    if user_form.is_valid() and customer_form.is_valid():
        user = user_form.save(commit=False)
        user.set_password(user_form.cleaned_data['password'])
        user.save()
        customer = customer_form.save(commit=False)
        customer.user = user
        customer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    else:
        errors = {**user_form.errors, **customer_form.errors}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)