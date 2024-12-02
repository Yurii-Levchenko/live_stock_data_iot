from django.contrib import admin
from .models import Stock, StockPrice

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name', 'sector')  # Fields shown in the list view
    search_fields = ('ticker', 'name', 'sector')  # Add search functionality
    list_filter = ('sector',)  # Add filter by sector

@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ('stock', 'price', 'timestamp')  # Fields shown in the list view
    search_fields = ('stock__ticker',)  # Allow searching by ticker
    list_filter = ('timestamp',)  # Add filter by timestamp
