from django.shortcuts import render
from .models import Product
from .forms import SearchForm
from django.http import HttpResponse

def index(request):
    inserts = Product.objects.all()
    form = SearchForm()
    return render(request, 'index.html', {'inserts': inserts, 'form': form})

def detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'detail.html', {'product': product})

def like_product(request):
    product_id = request.POST.get('product_id', None)

    likes = 0
    if (product_id):
        product = Product.objects.get(id=int(product_id))
        if product is not None:
            likes = product.likes + 1
            product.likes = likes
            product.save()
    return HttpResponse(likes)