from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify


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
    base_image = models.ImageField(upload_to='images', default='media/default.png', )

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images')
    image = models.ImageField(upload_to='images', default='media/default.png', )

    def __str__(self):
        return self.product.name


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
    slug = slugify(instance.name)
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



