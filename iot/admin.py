from django.contrib import admin
from .models import Device, DeviceSession

# @admin.register(Device)
# class DeviceAdmin(admin.ModelAdmin):
#     list_display = ('name', 'assigned_stock')  # Fields shown in the list view
#     search_fields = ('name', 'assigned_stock__ticker')  # Search by name or stock ticker


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'name', 'description', 'created_at', 'updated_at')

@admin.register(DeviceSession)
class DeviceSessionAdmin(admin.ModelAdmin):
    list_display = ('device', 'connected_at', 'disconnected_at', 'ip_address')
