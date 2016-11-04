from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    TYPES = (
        (1, 'Insert'),
        (2, 'Accessory')
    )
    name = models.CharField(max_length=40)
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
        return self.name


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


