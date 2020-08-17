from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from Operation.models import Product, Goods
from django.utils.formats import number_format
import locale
locale.setlocale(locale.LC_ALL, '')

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)
class prod_produce(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_pro = models.ForeignKey(Goods, on_delete=models.CASCADE)
    production_date = models.ForeignKey(Goods('date_produced'), related_name="date", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Product Produced"

class Production(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_pro = models.CharField(max_length=50)
    date_created = models.DateField(editable=False, auto_now_add=True)

    class Meta:
        verbose_name = "Produced"

class Customers(models.Model):
    customer_name = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.CharField(max_length=11)
    gender = models.CharField(max_length=1, choices=SEX_CHOICES, default='F')
    DOB = models.DateField(blank=True)

    def __str__(self):
        return self.customer_name        
        
class Demands(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    customer = models.ForeignKey(Customers, null=True, on_delete=models.CASCADE)
    date_sold = models.DateField(blank=True, null=True)
    product_price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(editable=False, auto_now_add=True)
    amount_paid = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-date_created']

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.product_price
        self.balance = (self.subtotal or 0) - self.amount_paid
        super(Demands, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.customer
       
class Sale(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_sold = models.DateTimeField(auto_now_add=True, auto_now=False)
    product_price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.product_price
        super(Sale, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.customer
