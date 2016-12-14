import qrcode
import random
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.urls import reverse
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToCover, Crop, Resize

from Flybletop.settings import BASE_DIR
from helpers.watermark import ImageWatermark
from ckeditor.fields import RichTextField
from django.utils.translation import ugettext_lazy as _


class Product(models.Model):
    TYPES = (
        (1, _('Product|Insert')),
        (2, _('Product|Accessory'))
    )
    name = models.CharField(max_length=40, verbose_name=_('Product|name'))
    slug = models.SlugField(unique=True, blank=True, verbose_name=_('Product|slug'))
    desc = models.TextField(verbose_name=_('Product|desc'))
    type = models.IntegerField(choices=TYPES, verbose_name=_('Product|type'))
    price_byn = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Product|BYN'))
    price_usd = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Product|USD'))
    base_image = ProcessedImageField(upload_to='images',
                                     processors=[ResizeToFit(300, 300)],
                                     format='PNG',
                                     default='media/default.png',
                                     verbose_name=_("Product|base_image"))
    base_image_thumbnail = ImageSpecField(source='base_image',
                                          processors=[ResizeToCover(100, 50)],
                                          format='PNG', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Product|created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Product|updated_at'))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Product|plural')

    def __str__(self):
        return self.name

    def admin_image_tag(self):
        return u'<img src="%s" />' % self.base_image_thumbnail.url

    admin_image_tag.allow_tags = True
    admin_image_tag.short_description = _('Product|image')


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', verbose_name=_('ProductImage|name'))
    image = ProcessedImageField(upload_to='images',
                                processors=[
                                    ResizeToFit(800, 600),
                                    ImageWatermark(
                                        'media/default_images/watermark.png',
                                    )
                                ],
                                format='PNG',
                                default='media/default.png',
                                verbose_name=_('ProductImage|image'))
    image_preview = ImageSpecField(source='image',
                                   processors=[ResizeToCover(300, 400)],
                                   format='PNG', )

    class Meta:
        verbose_name = _('ProductImage')
        verbose_name_plural = _('ProductImage|plural')

    def __str__(self):
        return self.product.name


class News(models.Model):
    body = RichTextField(verbose_name=_('News|body'))
    carousel = models.BooleanField(default=False, verbose_name=_('News|carousel'))
    image = ProcessedImageField(upload_to='images/base',
                                processors=[Resize(800, 600, False)],
                                format='JPEG',
                                verbose_name=_('News|image'))
    cropped_image = ImageSpecField(source='image',
                                   processors=[Crop(400, 400)],
                                   format='JPEG')
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToCover(100, 100)],
                                     format='JPEG', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('News|created'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('News|updated'))

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News|plural')

    def __str__(self):
        return str(self.id)

    def admin_image_tag(self):
        return u'<img src="%s" />' % self.image_thumbnail.url

    def admin_body(self):
        s = strip_tags(self.body)[:40]
        if len(strip_tags(self.body)) > 40:
            s += '...'
        return s

    admin_image_tag.allow_tags = True
    admin_body.allow_tags = True
    admin_body.short_description = _('News|body')
    admin_image_tag.short_description = _('News|Image')


class Like(models.Model):
    TYPES = (
        (1, 'Like'),
        (2, 'Favorite')
    )
    product = models.ForeignKey(Product, related_name='product_id')
    user = models.ForeignKey(User, related_name='user_id', default=None, null=True)
    like_type = models.IntegerField(choices=TYPES)
    ip_address = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    activation_key = models.CharField(max_length=40, null=True)
    key_expires = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.first_name


class Contact(models.Model):
    TYPES = (
        (1, _('Contact|social')),
        (2, _('Contact|other'))
    )

    title = models.CharField(max_length=20, blank=True, verbose_name=_('Contact|title'))
    url_text = models.CharField(max_length=50, blank=True, verbose_name=_('Contact|url_text'))
    url = models.CharField(max_length=100, verbose_name=_('Contact|url'))
    contact_type = models.IntegerField(choices=TYPES, verbose_name=_('Contact|type'))
    image = ProcessedImageField(upload_to='images/contacts',
                                processors=[Resize(20, 20, False)],
                                format='PNG',
                                verbose_name=_('Contact|image'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Contact|created'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Contact|updated'))

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contact|plural')

    def __str__(self):
        return self.title

    def admin_image(self):
        return u'<img src="%s" />' % self.image.url

    admin_image.allow_tags = True
    admin_image.short_description = _('Contact|image')


class AccessCode(models.Model):
    product = models.ForeignKey(Product, related_name='accesscode', verbose_name=_('Product|AccessCode'))
    code = models.CharField(max_length=40, unique=True, blank=True, verbose_name=_('AccessCode|code'))
    usage = models.BooleanField(default=False, verbose_name=_('AccessCode|usage'))
    qrcode = models.ImageField(upload_to='qrcode', blank=True, null=True, verbose_name=_('AccessCode|qrcode'))
    user = models.ForeignKey(User, related_name='user', verbose_name=('AccessCode|user'), null=True, blank=True)

    def generate_qrcode(self):
        qr = qrcode.QRCode(version=1, box_size=6, border=0)
        qr.add_data(self.code)
        qr.make(fit=True)
        img = qr.make_image()
        buffer = BytesIO()
        img.save(buffer)
        filename = 'qr-%s.png' % (self.id)
        filebuffer = InMemoryUploadedFile(buffer, None, filename, 'image/png', buffer.__sizeof__(), None)
        self.qrcode.save(filename, filebuffer, False)

    def admin_image(self):
        return u'<img src="%s" />' % self.qrcode.url

    def save(self, generate_qr=True, *args, **kwargs):
        if generate_qr:
            self.generate_qrcode()
        super(AccessCode, self).save(*args, **kwargs)

    admin_image.allow_tags = True
    admin_image.short_description = _('AccessCode|image')


def _create_slug(instance, new_slug=None):
    slug = slugify(instance.name_en)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return _create_slug(instance, new_slug=new_slug)
    return slug


def _create_access_code():
    num = '%s-%s-%s' % (random.randint(1000, 9990), random.randint(1000, 9990), random.randint(1000, 9990))
    check = AccessCode.objects.filter(code=num)
    if check.exists():
        return _create_access_code()
    return num


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = _create_slug(instance)


def pre_save_accesscode_receiver(sender, instance, *args, **kwargs):
    if not instance.code:
        instance.code = _create_access_code()


pre_save.connect(pre_save_product_receiver, sender=Product)
pre_save.connect(pre_save_accesscode_receiver, sender=AccessCode)
