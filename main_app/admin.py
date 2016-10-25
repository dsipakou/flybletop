from django.contrib import admin
from .models import Product, Image


class ImageAdminInline(admin.StackedInline):
    model = Image
    max_num = 10
    extra = 0


class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'type', 'price_byn')

    inlines = [ImageAdminInline, ]

admin.site.register(Product, ProductAdmin)
admin.site.register(Image)
