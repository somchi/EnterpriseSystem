from django.db import models
from django.db.models import Sum

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    quantity_produced = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, default=0)

    def __str__(self):
        return self.name

class Goods(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, editable=True)
    date_produced = models.DateTimeField(editable=False, auto_now_add=True)
    quantity_produced = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    class Meta:
        ordering =['date_produced']
