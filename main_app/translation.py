from modeltranslation.translator import register, TranslationOptions
from .models import Product, News, Contact, AccessCode


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'desc',)


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('body',)


@register(Contact)
class ContactTranslationOptions(TranslationOptions):
    fields = ('title', )


@register(AccessCode)
class AccessCodeTranslationOptions(TranslationOptions):
    fields = ()
