from django.contrib import admin
from .models import Employee, EmployeeType, Position, Unit, Bank, PayType

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('title','sex', 'phone')
admin.site.register(Employee,  EmployeeAdmin)
admin.site.register(EmployeeType)
admin.site.register(Unit)
admin.site.register(Position)
admin.site.register(Bank)
admin.site.register(PayType)

# Register your models here.
