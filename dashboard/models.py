from django.db import models
from django.utils import timezone

class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100, blank=True, null=True)
    market_status = models.CharField(max_length=50, blank=True, null=True, default='unknown')
    exchange = models.CharField(max_length=50, blank=True, null=True, default='unknown')
    latest_price_time = models.DateTimeField(blank=True, null=True) # Time of the latest known price for dashboard/UI


    def __str__(self):
        return self.ticker

class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_at = models.DateTimeField(default=timezone.now) # Time this price point was created

    def __str__(self):
        return f"{self.stock.ticker}: {self.price} at {self.recorded_at}"

    # def is_significant_change(self, new_price, threshold=0.01):
    #     if not self.price:
    #         return True
    #     try:
    #         diff = abs((float(new_price) - float(self.price)) / float(self.price))
    #         return diff >= threshold
    #     except ZeroDivisionError:
    #         return True

class DailyStockOHLC(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=12, decimal_places=4)
    high_price = models.DecimalField(max_digits=12, decimal_places=4)
    low_price = models.DecimalField(max_digits=12, decimal_places=4)
    close_price = models.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        unique_together = ('stock', 'date')
