from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Fields shown in the list view
    search_fields = ('user__username',)  # Allow searching by username
    filter_horizontal = ('favorite_tickers',)  # Add multi-select for favorite tickers
