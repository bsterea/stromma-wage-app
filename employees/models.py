from django.db import models
from stromma_employees.models import Employee


class PayrollRecord(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="payroll_records",
    )
    period_year = models.PositiveIntegerField()
    period_month = models.PositiveIntegerField()
    normal_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deduction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gross_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-period_year", "-period_month", "employee__last_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "period_year", "period_month"],
                name="unique_employee_payroll_period",
            )
        ]

    def __str__(self):
        return f"{self.employee} - {self.period_month:02d}/{self.period_year}"