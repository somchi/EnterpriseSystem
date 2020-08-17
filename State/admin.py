from django.contrib import admin 
from .models import State, Country, LGA

admin.site.register(State)
admin.site.register(Country)
admin.site.register(LGA)
# Register your models here.
