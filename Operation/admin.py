from django.contrib import admin
from .models import Goods, Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', )

class GoodsAdmin(admin.ModelAdmin):
    list_display = ('product_name', )

admin.site.register(Goods, GoodsAdmin)
admin.site.register(Product, ProductAdmin)
# Register your models here.
