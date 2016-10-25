from django.shortcuts import render
from .models import Product, Image
from .forms import SearchForm, LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(u, p)
                    return HttpResponseRedirect('/')
                else:
                    print('User is not active')
            else:
                print("User is not exist")
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def index(request):
    inserts = Product.objects.all()
    form = SearchForm()
    return render(request, 'index.html', {'inserts': inserts, 'form': form})


def detail(request, product_id):
    product = Product.objects.get(id=product_id)
    images = product.images.all()
    return render(request, 'detail.html', {'product': product, 'images': images})


def insert(request):
    inserts = Product.objects.filter(type=1)
    return render(request, 'insert/insert.html', {'inserts': inserts})


def accessory(request):
    accs = Product.objects.filter(type=2)
    return render(request, 'accessory/accessory.html', {'accs': accs})


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