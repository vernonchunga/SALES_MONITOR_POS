from django.shortcuts import render, redirect
from .models import *
from .forms import ProductForm, CustomerForm

# product views
def product_list(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, "product_list.html", context)

def Product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')
    else:
        form = ProductForm()

    context = {
        "ProductForm" : form
    }        
    return render(request, "product_add.html", context)

def product_update(request, id):
    product = Product.objects.get(id=id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProductForm(instance=product)

    context = {
        "form" : form
    }

    return render(request, "product_update.html", context)

def product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('/')






def add_customer(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid:
            customer_form.save()
            return redirect('/')
    else:
        customer_form = CustomerForm()

    context = {
        "customer_form": customer_form
    }    

    return render(request, "add_customer.html", context)        