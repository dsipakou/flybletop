import hashlib
import random

from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from .models import Product, Like, News, Profile, AccessCode
from .forms import SearchForm, LoginForm, RegistrationForm, RecoveryForm, NewPasswordForm, ActivationForm, ProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.utils.translation import ugettext_lazy as _

import json

url_skip_filter = [
    'login',
    'logout',
    'recovery'
]


def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            u = get_user(email)
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    url = request.POST.get('next', request.GET.get('next', '/'))
                    if url.replace('/', '') not in url_skip_filter:
                        return HttpResponseRedirect(url)
                    else:
                        return HttpResponseRedirect('/')
                else:
                    form.add_error(None, _('User is not activated'))
                    return render(request, 'authentication/login.html', {'form': form})
            else:
                form.add_error(None, _('Cannot login check credentials'))
                context = {
                    'form': form,
                    'next': request.POST.get('next', request.GET.get('next', '/'))
                }
                return render(request, 'authentication/login.html', context)
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
            form.save(data)
            user = authenticate(username=data['username'], password=data['password1'])
            login(request, user)
            url = request.POST.get('next', request.GET.get('next', '/'))
            if url:
                return HttpResponseRedirect(url)
            else:
                template = loader.get_template('authentication/registered.html')
                return HttpResponse(template.render())
        else:
            context = {
                'form': form,
                'next': request.POST.get('next', request.GET.get('next', '/'))
            }
            return render(request, 'authentication/signup.html', context)
    else:
        form = RegistrationForm()
        context = {
            'form': form,
            'next': request.GET.get('next')
        }
        return render(request, 'authentication/signup.html', context)


def recovery(request):
    if request.method == 'POST':
        form = RecoveryForm(request.POST)
        if form.is_valid():
            context = {}
            data = dict()
            data['email'] = form.cleaned_data['email']
            rand_name = str(random.random()).encode('utf8')
            salt = hashlib.sha1(rand_name).hexdigest()[:5]
            usernamesalt = data['email'] + salt
            data['activation_key'] = hashlib.sha1(usernamesalt.encode('utf8')).hexdigest()
            data['email_body'] = _('test email body')
            data['email_subject'] = _('Password reset email')
            data['url'] = request.build_absolute_uri()
            form.send_email(data)
            context['form'] = form
            messages.success(request, _('check e-mail'))
            return render(request, 'authentication/recovery.html', context)
        else:
            context = {
                'form': form,
                'next': request.POST.get('next', request.GET.get('next', '/'))
            }
            return render(request, 'authentication/signup.html', context)
    else:
        if request.user is not None and request.user.is_authenticated:
            auth.logout(request)
        form = RecoveryForm()
        return render(request, 'authentication/recovery.html', {'form': form})


def password_reset(request, activation_key):
    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            data = dict()
            data['activation_key'] = activation_key
            data['password1'] = form.cleaned_data['password1']
            form.reset(data)
            template = loader.get_template('authentication/reset_completed.html')
            return HttpResponse(template.render())
        else:
            return render(request, 'authentication/password_reset.html', {'form': form})
    else:
        profile = Profile.objects.filter(activation_key=activation_key)
        if len(profile) > 0:
            if timezone.now() > profile[0].key_expires:
                messages.error(request, _('key expires'))
                return HttpResponseRedirect(reverse('recovery'))
            else:
                form = NewPasswordForm()
                return render(request, 'authentication/password_reset.html', {'form': form})
        else:
            messages.error(request, _('activation key is not found'))
            return HttpResponseRedirect(reverse('recovery'))


@login_required
def logout_view(request):
    logout(request)
    url = request.GET.get('next', '/')
    return HttpResponseRedirect(url)


def index(request):
    news = News.objects.filter(carousel=False)
    carousel = News.objects.filter(carousel=True)
    searchForm = SearchForm()
    context = {
        'news': news,
        'carousel': carousel,
        'searchForm': searchForm
    }

    return render(request, 'main/index.html', context)


def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    fav = len(Like.objects.filter(product_id=product, user_id=request.user.id, like_type=2)) > 0
    base_template = 'insert/base.html' if product.type == 1 else 'accessory/base.html'
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
    if request.method == 'POST':
        form = ProfileForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile updated successfully'))
        context = {
            'form': form
        }
        return render(request, 'user/profile.html', context)
    else:
        form = ProfileForm()
        form.fields['email'].initial = request.user.email
        form.fields['username'].initial = request.user.username
        context = {
            'form': form
        }
        return render(request, 'user/profile.html', context)


@login_required
def favorite(request):
    products = Product.objects.filter(product_id__like_type=2, product_id__user=request.user.id)
    types = {'1': 'insert', '2': 'accessory'}
    context = {
        'products': products,
        'types': types
    }
    return render(request, 'user/favorite.html', context)


@login_required
def my_products(request):
    codes = AccessCode.objects.filter(user=request.user, activated=True)
    context = {
        'codes': codes
    }
    return render(request, 'user/products.html', context)

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


def contacts(request):
    return render(request, 'contacts/contacts.html')


def activate_product(request, activation_key=False):
    url = '/activate/'
    if activation_key:
        url += activation_key
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ActivationForm(request.POST)
            if form.is_valid():
                data = {
                    'code': form.cleaned_data['code']
                }
                get_code = AccessCode.objects.filter(code=data['code'])
                if len(get_code) < 1:
                    form.add_error('code', _('No such access code'))
                    return render(request, 'activation/activate.html', {'form': form})
                elif get_code[0].activated:
                    form.add_error('code', _('Code already used'))
                    return render(request, 'activation/activate.html', {'form': form})
                else:
                    get_code[0].activated = True
                    get_code[0].user = request.user
                    get_code[0].save()
                    return render(request, 'activation/activate.html', {'success': True})
        else:
            form = ActivationForm()
            if activation_key:
                form.fields['code'].initial = activation_key
            context = {
                'form': form
            }
            return render(request, 'activation/activate.html', context)
    else:
        return HttpResponseRedirect(reverse('login') + '?next=' + url)


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


@login_required
def favorite_product(request):
    response_data = {}
    product_id = request.POST.get('product_id', None)
    product = Product.objects.get(id=int(product_id))
    if product_id and product_id.isdigit():
        fav = Like.objects.filter(user_id=request.user.id, product_id=product, like_type=2).first()
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
