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
