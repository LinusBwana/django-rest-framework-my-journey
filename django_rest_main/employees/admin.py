from django.contrib import admin
from .models import Employee

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['emp_id', 'emp_name', 'designation']

admin.site.register(Employee, EmployeeAdmin)