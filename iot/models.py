# iot/models.py
from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100)
    assigned_stock = models.ForeignKey('dashboard.Stock', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
