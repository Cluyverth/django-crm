from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import SignUpForm, AddCustomerForm
from .models import Customer

# Create your views here.
def home(request):
    
    customers = Customer.objects.all()
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was an error logged in, please try again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'customers':customers})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have Successfully Registered!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})

def customer_info(request, pk):
    if request.user.is_authenticated:
        customer_info = Customer.objects.get(id=pk)
        return render(request, 'customer.html', {'customer_info':customer_info})
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('home')
    
def delete_customer(request, pk):
    if request.user.is_authenticated:
        del_customer = Customer.objects.get(id=pk)
        del_customer.delete()
        messages.success(request, f"Customer {del_customer} deleted successfully!")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to delete someone!")
        return redirect('home')
    
def add_customer(request):
    form = AddCustomerForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_customer = form.save()
                messages.success(request, f"Customer {add_customer} created successfully!")
                return redirect('home')
        return render(request, 'add_customer.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to create a customer!")
        return redirect('home')
    
def update_customer(request, pk):
    if request.user.is_authenticated:
        current_customer = Customer.objects.get(id=pk)
        form = AddCustomerForm(request.POST or None, instance=current_customer)
        if form.is_valid():
            form.save()    
            messages.success(request, f"Customer {current_customer} updated successfully!")
            return redirect('home')
        return render(request, 'update_customer.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to update someone!")
        return redirect('home')