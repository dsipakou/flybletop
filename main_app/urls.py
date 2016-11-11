from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^signup/', views.signup_view, name='sign_up'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^$', views.index),
    url(r'^insert/(?P<slug>[^/]+)/$', views.detail, name='ins_detail'),
    url(r'^accessory/(?P<slug>[^/]+)/$', views.detail, name='acc_detail'),
    url(r'^insert/$', views.insert, name='insert'),
    url(r'^accessory/$', views.accessory, name='accessory'),
    url(r'^favorite_product/$', views.favorite_product, name='favorite_product'),
    url(r'^like_product/$', views.like_product, name='like_product'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,})
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, })
    ]