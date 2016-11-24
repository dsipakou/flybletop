from django.contrib import admin
from .models import Product, ProductImage, News
from modeltranslation.admin import TranslationAdmin


class ImageAdminInline(admin.StackedInline):
    model = ProductImage
    max_num = 10
    extra = 0


class ProductAdmin(TranslationAdmin):
    list_display = ('admin_image_tag', 'name', 'type', 'price_byn', 'created_at', 'updated_at')

    inlines = [ImageAdminInline, ]


class NewsAdmin(TranslationAdmin):
    list_display = ('id', 'admin_body', 'admin_image_tag', 'created_at', 'updated_at')


admin.site.register(Product, ProductAdmin)
admin.site.register(News, NewsAdmin)
