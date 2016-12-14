from django.contrib import admin
from .models import Product, ProductImage, News, Contact, AccessCode
from modeltranslation.admin import TranslationAdmin


class ImageAdminInline(admin.StackedInline):
    model = ProductImage
    max_num = 10
    extra = 0


class AccessCodeAdminInline(admin.StackedInline):
    model = AccessCode
    max_num = 100
    extra = 0
    exclude = ('qrcode',)


class ProductAdmin(TranslationAdmin):
    list_display = ('admin_image_tag', 'name', 'type', 'price_byn', 'created_at', 'updated_at')

    inlines = [ImageAdminInline, AccessCodeAdminInline, ]


class NewsAdmin(TranslationAdmin):
    list_display = ('id', 'admin_body', 'admin_image_tag', 'carousel', 'created_at', 'updated_at')
    list_filter = ('carousel',)


class ContactAdmin(TranslationAdmin):
    list_display = ('title', 'admin_image', 'url_text', 'contact_type', 'created_at', 'updated_at')


class AccessCodeAdmin(TranslationAdmin):
    list_display = ('product', 'code', 'usage', 'admin_image', 'user')
    exclude = ('qrcode', 'code', 'user', 'usage')
    list_filter = ('product', 'usage')


admin.site.register(Product, ProductAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(AccessCode, AccessCodeAdmin)