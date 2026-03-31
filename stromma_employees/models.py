from django.db import models


class Role(models.Model):
    ROLE_CHOICES = [
        ("driver", "Driver"),
        ("supervisor", "Supervisor"),
        ("trainer", "Trainer"),
    ]

    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    EMPLOYMENT_STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("sick", "Sick"),
        ("vacation", "Vacation"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cpr = models.CharField(max_length=20, unique=True)

    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    hire_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_STATUS_CHOICES,
        default="active",
    )

    roles = models.ManyToManyField(Role, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ---------------------------
# NEW: Season
# ---------------------------
class Season(models.Model):
    name = models.CharField(max_length=100, unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.valid_from} - {self.valid_to})"


# ---------------------------
# NEW: ShiftTemplate
# ---------------------------
class ShiftTemplate(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("validated", "Validated"),
        ("ready", "Ready for allocation"),
        ("invalid", "Invalid"),
        ("overridden", "Overridden"),
    ]

    ROLE_REQUIRED_CHOICES = [
        ("driver", "Driver"),
        ("supervisor", "Supervisor"),
        ("trainer", "Trainer"),
    ]

    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100, blank=True)

    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name="shift_templates"
    )

    valid_from = models.DateField()
    valid_to = models.DateField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    role_required = models.CharField(
        max_length=20,
        choices=ROLE_REQUIRED_CHOICES,
        default="driver"
    )

    notes = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code", "valid_from"]
        unique_together = ("code", "season", "valid_from", "valid_to")

    def __str__(self):
        return f"{self.code} - {self.season.name}"


# ---------------------------
# NEW: ShiftBreak (PAUZE)
# ---------------------------
class ShiftBreak(models.Model):
    shift_template = models.ForeignKey(
        ShiftTemplate,
        on_delete=models.CASCADE,
        related_name="breaks"
    )

    break_order = models.PositiveIntegerField(default=1)

    break_start = models.TimeField()
    break_end = models.TimeField()

    is_paid = models.BooleanField(default=False)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["shift_template", "break_order"]
        unique_together = ("shift_template", "break_order")

    def __str__(self):
        return f"{self.shift_template.code} - Break {self.break_order}"
