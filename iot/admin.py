from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'assigned_stock')  # Fields shown in the list view
    search_fields = ('name', 'assigned_stock__ticker')  # Search by name or stock ticker
