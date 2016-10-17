from django.shortcuts import render
from .models import Product
from .forms import SearchForm

def index(request):
    inserts = Product.objects.all()
    form = SearchForm()
    return render(request, 'index.html', {'inserts': inserts, 'form': form})

def detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'detail.html', {'product': product})