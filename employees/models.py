from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from companies.models import Company


class Employee(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    photo = models.ImageField(upload_to='images/')
    position = models.CharField(max_length=64)
    salary = models.DecimalField(max_digits=8, decimal_places=2,
                                 validators=[MinValueValidator(Decimal('0.01'))])
    employer = models.ForeignKey(
        Company,
        null=True,
        on_delete=models.SET_NULL,
        related_name='employees'
    )

    def __str__(self):
        return f'{self.pk} - {self.first_name} {self.last_name} - {self.position}'
