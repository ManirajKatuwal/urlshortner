# shortener/admin.py
from django.contrib import admin
from .models import ShortURL, Click

@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('slug', 'owner', 'original_url', 'created_at', 'click_count', 'expires_at')
    search_fields = ('slug', 'original_url', 'owner__username')

@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ('shorturl', 'timestamp', 'ip_address')
    list_filter = ('timestamp',)
