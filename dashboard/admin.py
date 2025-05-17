from django.contrib import admin
from .models import Stock, StockPrice

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name', 'sector', 'market_status', 'exchange', 'latest_price_time')  # Fields shown in the list view
    search_fields = ('ticker', 'name', 'sector',)  # search
    list_filter = ('sector', 'market_status', 'exchange')  # filter by sector

@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ('stock', 'price', 'recorded_at')  # Fields shown in the list view
    search_fields = ('stock__ticker',)  # Allow searching by ticker
    list_filter = ('recorded_at',)  # Add filter by timestamp
