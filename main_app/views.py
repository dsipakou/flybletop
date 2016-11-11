import hashlib
import random

from django.shortcuts import get_object_or_404, render
from .models import Product, Like
from .forms import SearchForm, LoginForm, RegistrationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
import json


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    url = request.POST.get('next', request.GET.get('next', '/'))
                    return HttpResponseRedirect(url)
                else:
                    form.add_error(None, _('User is not activated'))
                    return render(request, 'authentication/login.html', {'form': form})
            else:
                form.add_error(None, 'Cannot login. Please, check your credentials.')
                return render(request, 'authentication/login.html', {'form': form})
    else:
        form = LoginForm()
        next = request.GET.get('next')
        context = {
            'form': form,
            'next': next
        }
        return render(request, 'authentication/login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = {}
            data['username'] = form.cleaned_data['username']
            data['email'] = form.cleaned_data['email']
            data['password1'] = form.cleaned_data['password1']
            salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            usernamesalt = data['username']
            data['activation_key'] = hashlib.sha1((salt+usernamesalt).encode('utf-8')).hexdigest()
            data['email_path'] = '/ActivationEmail.txt'
            data['email_subject'] = 'Activate your account on FlybleTop'
            #form.sendEmail(data)
            form.save(data)
            url = request.GET.get('next', '')
            return HttpResponseRedirect(url)
        else:
            return render(request, 'authentication/signup.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'authentication/signup.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    url = request.GET.get('next', '/')
    return HttpResponseRedirect(url)


def index(request):
    inserts = Product.objects.all()
    form = SearchForm()
    context = {
        'inserts': inserts,
        'form': form
    }
    return render(request, 'index.html', context)


def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    fav = len(Like.objects.filter(product_id=product, user_id=request.user.id, like_type=2)) > 0
    base_template = 'insert/base.html' if product.get_type_display() == 'Insert' else 'accessory/base.html'
    images = product.images.all()
    likes = len(Like.objects.filter(product_id=product, like_type=1))
    if request.user.id is not None:
        like = len(Like.objects.filter(user_id=request.user.id, product_id=product, like_type=1)) > 0
    else:
        like = len(Like.objects.filter(ip_address=get_user_ip(request), product_id=product, like_type=1)) > 0
    context = {
        'product': product,
        'images': images,
        'base_template': base_template,
        'likes': likes,
        'fav': fav,
        'like': like
    }
    return render(request, 'details/detail.html', context)


@login_required
def profile(request):
    products = Product.objects.filter(product_id__like_type=2, product_id__user=request.user.id)
    context = {
        'products': products
    }
    return render(request, 'user/profile.html', context)


def insert(request):
    inserts = Product.objects.filter(type=1)
    context = {
        'inserts': inserts
    }
    return render(request, 'insert/insert.html', context)


def accessory(request):
    accs = Product.objects.filter(type=2)
    context = {
        'accs': accs
    }
    return render(request, 'accessory/accessory.html', context)


def like_product(request):
    response_data = {}
    product_id = request.POST.get('product_id', None)
    if product_id:
        if request.user.id is not None:
            like = Like.objects.filter(user_id=request.user.id, product_id=int(product_id), like_type=1).first()
        else:
            like = Like.objects.filter(ip_address=get_user_ip(request), product_id=int(product_id), like_type=1).first()
        if like:
            like.delete()
            likes = len(Like.objects.filter(product_id=int(product_id), like_type=1))
            response_data['result'] = 'deleted'
            response_data['likes'] = likes
        else:
            like = Like(product_id=product_id, like_type=1, ip_address=get_user_ip(request), user_id=request.user.id)
            like.save()
            likes = len(Like.objects.filter(product_id=int(product_id), like_type=1))
            response_data['result'] = 'added'
            response_data['likes'] = likes
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def favorite_product(request):
    response_data = {}
    product_id = request.POST.get('product_id', None)
    product = Product.objects.get(id=int(product_id))
    if product_id and product_id.isdigit():
        fav = Like.objects.filter(user_id=request.user.id, product_id=product).first()
        if fav:
            fav.delete()
            response_data['result'] = 'deleted'
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            fav = Like(product=product, like_type=2, ip_address=get_user_ip(request), user_id=request.user.id)
            fav.save()
            response_data['result'] = 'added'
            return HttpResponse(json.dumps(response_data), content_type='application/json')
    response_data['result'] = 'error'
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def get_user_ip(request):
    ip = request.META.get('CF-Connecting-IP')
    if ip is None:
        ip = request.META.get('REMOTE_ADDR')
    return ip
