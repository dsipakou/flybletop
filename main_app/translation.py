from modeltranslation.translator import register, TranslationOptions
from .models import Product, News


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('body',)
