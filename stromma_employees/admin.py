from django.contrib import admin
from .models import (
    Employee,
    Role,
    WorkProgram,
    ShiftTemplate,
    ShiftBreak,
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "cpr", "status", "is_active")
    search_fields = ("first_name", "last_name", "cpr")
    list_filter = ("status", "is_active")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(WorkProgram)
class WorkProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "valid_from", "valid_to", "status", "is_active")
    search_fields = ("name",)
    list_filter = ("status", "is_active")


class ShiftBreakInline(admin.TabularInline):
    model = ShiftBreak
    extra = 1


@admin.register(ShiftTemplate)
class ShiftTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "work_program",
        "valid_from",
        "valid_to",
        "start_time",
        "end_time",
        "role_required",
        "status",
        "is_active",
    )
    search_fields = ("code", "name")
    list_filter = ("work_program", "role_required", "status", "is_active")
    inlines = [ShiftBreakInline]
