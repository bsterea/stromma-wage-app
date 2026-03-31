from django.contrib import admin
from .models import (
    Employee,
    Role,
    WorkProgram,
    ShiftTemplate,
    ShiftBreak,
    LegalRule,
    ShiftValidation,
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


class ShiftValidationInline(admin.TabularInline):
    model = ShiftValidation
    extra = 0
    readonly_fields = ("rule", "status", "message", "checked_at")
    can_delete = False


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
    inlines = [ShiftBreakInline, ShiftValidationInline]


@admin.register(LegalRule)
class LegalRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "rule_type", "valid_from", "valid_to", "is_active")
    search_fields = ("name", "source")
    list_filter = ("rule_type", "is_active")


@admin.register(ShiftValidation)
class ShiftValidationAdmin(admin.ModelAdmin):
    list_display = ("shift_template", "rule", "status", "checked_at", "overridden")
    list_filter = ("status", "overridden")
    search_fields = ("shift_template__code", "rule__name")
