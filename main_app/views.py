from django.shortcuts import render
from .models import Product

def index(request):
    inserts = Product.objects.all()
    return render(request, 'index.html', {'inserts': inserts})

def detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'detail.html', {'product': product})