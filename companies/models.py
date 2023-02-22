from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=64, unique=True)
    logo = models.FileField(upload_to='logos/')
    description = models.TextField(max_length=300)

    def __str__(self):
        return f'{self.pk} - {self.name}'
