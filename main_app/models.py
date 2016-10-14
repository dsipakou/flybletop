from django.db import models

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

    def __str__(self):
        return self.name