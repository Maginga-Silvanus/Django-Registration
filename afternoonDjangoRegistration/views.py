from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Product


def register(request):
    if request.method == "POST":
        form =UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for {username }')
            return redirect('users-registration')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def add_product(request):
    if request.method == "POST":
        product_name = request.POST.get('p_name')
        product_price = request.POST.get('p_price')
        product_quantity = request.POST.get('p_quantity')
        # Save data into the database
        product = Product(prod_name= product_name,
                          prod_price= product_price,
                          prod_quantity= product_quantity)
        product.save()
        messages.success(request,"Data saved successfully")
        return redirect("add-product")

    return render(request, 'add-products.html')


@login_required
def view_products(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'products.html', context)