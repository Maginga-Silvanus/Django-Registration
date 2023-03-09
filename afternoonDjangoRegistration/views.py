from __future__ import unicode_literals
from django_daraja.mpesa import utils
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django_daraja.mpesa.core import MpesaClient
from decouple import config
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Supplier


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


@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request,'Product deleted successfully')
    return redirect("products")


@login_required
def update_product(request, id):
    if request.method == "POST":
        product_name = request.POST.get("p_name")
        product_price = request.POST.get("p_price")
        product_quantity = request.POST.get("p_quantity")

        # select the product you want to update
        product = Product.objects.get(id=id)

        # update the product
        product.prod_name = product_name
        product.prod_quantity = product_quantity
        product.prod_price = product_price

        # Return the updated values back to the database
        product.save()
        messages.success(request,'Product updated successfully')
        return redirect('products')

    product = Product.objects.get(id=id)
    return render(request, 'update.html', {'product':product})


@login_required
def add_supplier(request):
    if request.method == "POST":
        name = request.POST.get('s_name')
        email = request.POST.get('s_email')
        phone= request.POST.get('s_phone')
        product = request.POST.get('s_product')
        # Save data into the database
        supplier = Supplier(sup_name=name,
                          suo_email=email,
                          sup_phone=phone,
                            sup_product= product)
        supplier.save()
        messages.success(request,"Supplier saved successfully")
        return redirect('add-supplier')

    return render(request, 'add-supplier.html')


@login_required
def view_supplier(request):
    suppliers = Supplier.objects.all()
    context = {'suppliers':suppliers}
    return render(request, 'suppliers.html', context)


@login_required
def delete_supplier(request, id):
    supplier= Supplier.objects.get(id=id)
    supplier.delete()
    messages.success(request, 'supplier deleted successfully')
    return redirect('suppliers')


@login_required
def update_supplier(request, id):
    if request.method == "POST":
        supplier_name = request.POST.get("s_name")
        supplier_email = request.POST.get("s_email")
        supplier_phone = request.POST.get("s_phone")
        supplier_product = request.POST.get("s_product")

        # select the product you want to update
        supplier = Supplier.objects.get(id=id)

        # update the product
        supplier.sup_name= supplier_name
        supplier.suo_email = supplier_email
        supplier.sup_phone = supplier_phone
        supplier.sup_product = supplier_product

        # Return the updated values back to the database
        supplier.save()
        messages.success(request, 'Supplier updated successfully')
        return redirect('suppliers')

    supplier = Supplier.objects.get(id=id)
    return render(request, 'update-supplier.html', {'supplier': supplier})


cl = MpesaClient()
stk_callback_url = 'https://api.darajambili.com/express-payment'
b2c_callback_url = "https://api.darajambili.com/b2c/result"


def auth_success(request):
    token = cl.access_token()
    return JsonResponse(token, safe=False)


@login_required
def pay(request, id):
    # select the product being paid for
    product =Product.objects.get(id=id)
    if request.method == "POST":
        phone_number = request.POST.get('nambari')
        amount = request.POST.get('pesa')
        amount = int(amount)
        account_ref = "silva"
        transaction_desc = "Payment for goods"
        transaction = cl.stk_push(phone_number, amount, account_ref,transaction_desc,stk_callback_url)

        return JsonResponse(transaction.response_description, safe=False)
    return render(request, 'payment.html', {'product':product})