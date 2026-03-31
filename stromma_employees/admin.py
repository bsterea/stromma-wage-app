from django.contrib import admin
from .models import Employee, Role


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "cpr", "status", "is_active")
    search_fields = ("first_name", "last_name", "cpr")
    list_filter = ("status", "is_active")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
