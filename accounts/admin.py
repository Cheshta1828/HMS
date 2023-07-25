from django.contrib import admin

# Register your models here.
from .models import customuser
from .models import Department, PatientRecord

admin.site.register(Department)
admin.site.register(PatientRecord)
admin.site.register(customuser)