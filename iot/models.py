from django.db import models


class Device(models.Model):
    device_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # assigned_stock = models.ForeignKey('dashboard.Stock', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.device_id


class DeviceSession(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="sessions")
    connected_at = models.DateTimeField(auto_now_add=True)
    disconnected_at = models.DateTimeField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        status = "Connected" if not self.disconnected_at else "Disconnected"
        return f"{self.device.device_id} - {status} at {self.connected_at}"


# class Device(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name