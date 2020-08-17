from django.contrib import admin
from .models import Batch, EmployeePaySummary, BatchPayType

admin.site.register(Batch)
admin.site.register(EmployeePaySummary)
admin.site.register(BatchPayType)
