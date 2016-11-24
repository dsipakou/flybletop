from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.html import strip_tags
from django.utils.text import slugify
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToCover
from helpers.watermark import ImageWatermark
from ckeditor.fields import RichTextField


class Product(models.Model):
    TYPES = (
        (1, 'Insert'),
        (2, 'Accessory')
    )
    name = models.CharField(max_length=40)
    slug = models.SlugField(unique=True, null=True, blank=True)
    desc = models.TextField()
    type = models.IntegerField(choices=TYPES)
    price_byn = models.DecimalField(max_digits=5, decimal_places=2)
    price_usd = models.DecimalField(max_digits=5, decimal_places=2)
    base_image = ProcessedImageField(upload_to='images',
                                     processors=[ResizeToFit(300, 300)],
                                     format='PNG',
                                     default='media/default.png', )
    base_image_thumbnail = ImageSpecField(source='base_image',
                                          processors=[ResizeToCover(100, 50)],
                                          format='PNG',)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def admin_image_tag(self):
        return u'<img src="%s" />' % self.base_image_thumbnail.url

    admin_image_tag.allow_tags = True
    admin_image_tag.short_description = "Image"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images')
    image = ProcessedImageField(upload_to='images',
                                processors=[
                                    ResizeToFit(800, 600),
                                    ImageWatermark(
                                        'media/default_images/watermark.png',
                                    )
                                ],
                                format='PNG',
                                default='media/default.png', )
    image_preview = ImageSpecField(source='image',
                                   processors=[ResizeToCover(300, 400)],
                                   format='PNG', )

    def __str__(self):
        return self.product.name


class News(models.Model):
    body = RichTextField()
    image = ProcessedImageField(upload_to='images/base',
                                processors=[ResizeToFit(400, 400)],
                                format='PNG')
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToCover(100, 100)],
                                     format='PNG',)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    admin_image_tag.short_description = "Image"


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
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()

    def __str__(self):
        return self.name


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name_en)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_product_receiver, sender=Product)



