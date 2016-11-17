from django.contrib import admin
from .models import Product, Image
from modeltranslation.admin import TranslationAdmin


class ImageAdminInline(admin.StackedInline):
    model = Image
    max_num = 10
    extra = 0


class ProductAdmin(TranslationAdmin):

    list_display = ('admin_image_tag', 'name', 'type', 'price_byn', )

    inlines = [ImageAdminInline, ]

admin.site.register(Product, ProductAdmin)
admin.site.register(Image)
