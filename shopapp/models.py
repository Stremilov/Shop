from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _



def product_preview_directory_path(instance: 'Product', filename):
    return 'products/product_{pk}/preview/{filename}'.format(pk=instance.pk, filename=filename)


class Models(models.Model):
    class Meta:
        ordering = ['price']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    name = models.CharField(max_length=50)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)


    def __str__(self) -> str:
        return f'Model(pk={self.pk}, name={self.name!r})'


class Order(models.Model):
    class META:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    delivery_adress = models.TextField(null=False, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Models, related_name='orders')
    reciept = models.FileField(null=True, upload_to='orders/reciepts/')
