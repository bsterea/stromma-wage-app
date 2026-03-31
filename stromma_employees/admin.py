from django.contrib import admin
from .models import Employee, Role, Season, ShiftTemplate


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "cpr", "status", "is_active")
    search_fields = ("first_name", "last_name", "cpr")
    list_filter = ("status", "is_active")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("name", "valid_from", "valid_to")
    search_fields = ("name",)


@admin.register(ShiftTemplate)
class ShiftTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "season",
        "valid_from",
        "valid_to",
        "start_time",
        "end_time",
        "role_required",
        "status",
        "is_active",
    )
    search_fields = ("code", "name")
    list_filter = ("season", "role_required", "status", "is_active")
