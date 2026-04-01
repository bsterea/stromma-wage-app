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


class WorkProgram(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("archived", "Archived"),
    ]

    name = models.CharField(max_length=100)
    valid_from = models.DateField()
    valid_to = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-valid_from", "name"]

    def __str__(self):
        return f"{self.name} ({self.valid_from} - {self.valid_to})"


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

    work_program = models.ForeignKey(
        WorkProgram,
        on_delete=models.CASCADE,
        related_name="shift_templates"
    )

    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100, blank=True)

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
        unique_together = ("work_program", "code", "valid_from", "valid_to")

    def __str__(self):
        return f"{self.code} - {self.work_program.name}"


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


class LegalRule(models.Model):
    RULE_TYPE_CHOICES = [
        ("break", "Break rule"),
        ("rest", "Rest rule"),
        ("daily_limit", "Daily working limit"),
        ("weekly_limit", "Weekly working limit"),
        ("monthly_limit", "Monthly working limit"),
        ("days_pattern", "Working days pattern"),
        ("notice", "Notice rule"),
        ("informative", "Informative rule"),
    ]

    SEVERITY_CHOICES = [
        ("info", "Info"),
        ("warning", "Warning"),
        ("blocking", "Blocking"),
    ]

    UNIT_CHOICES = [
        ("minutes", "Minutes"),
        ("hours", "Hours"),
        ("days", "Days"),
        ("weeks", "Weeks"),
        ("months", "Months"),
        ("count", "Count"),
        ("text", "Text only"),
    ]

    name = models.CharField(max_length=200)
    rule_type = models.CharField(max_length=30, choices=RULE_TYPE_CHOICES)
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default="info",
    )

    numeric_value_1 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Primary numeric value"
    )

    numeric_value_2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Secondary numeric value"
    )

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default="text",
    )

    source = models.CharField(
        max_length=200,
        help_text="Example: Turistoverenskomst 2025-2028"
    )

    description = models.TextField(blank=True)

    valid_from = models.DateField()
    valid_to = models.DateField()

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name", "valid_from"]

    def __str__(self):
        return f"{self.name} ({self.rule_type})"


class ShiftValidation(models.Model):
    STATUS_CHOICES = [
        ("valid", "Valid"),
        ("warning", "Warning"),
        ("invalid", "Invalid"),
    ]

    shift_template = models.ForeignKey(
        ShiftTemplate,
        on_delete=models.CASCADE,
        related_name="validations"
    )

    rule = models.ForeignKey(
        LegalRule,
        on_delete=models.CASCADE
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    message = models.TextField()

    can_override = models.BooleanField(default=True)
    overridden = models.BooleanField(default=False)

    overridden_by = models.CharField(max_length=100, blank=True)
    override_reason = models.TextField(blank=True)

    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shift_template.code} - {self.status}"
