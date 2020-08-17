from django.contrib import admin
from .models import Demands, prod_produce, Sale, Customers

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', )

class SaleAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_sale', )

class SaleDetailAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'product_price', )

admin.site.register(Demands)
admin.site.register(prod_produce)
admin.site.register(Customers, CustomerAdmin)
admin.site.register(Sale, SaleDetailAdmin)

