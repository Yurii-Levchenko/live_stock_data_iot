from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StockPrice, Stock

@receiver(post_save, sender=StockPrice)
def update_latest_price_time(sender, instance, created, **kwargs):
    if created:
        stock = instance.stock
        stock.latest_price_time = instance.recorded_at
        stock.save(update_fields=['latest_price_time'])
