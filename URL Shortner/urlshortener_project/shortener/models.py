# shortener/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class ShortURL(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='short_urls')
    original_url = models.URLField()
    slug = models.CharField(max_length=100, unique=True, db_index=True)  # short key
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField(null=True, blank=True)  # expiration
    custom = models.BooleanField(default=False)  # user supplied slug

    def __str__(self):
        return f"{self.slug} -> {self.original_url}"

    def is_expired(self):
        if self.expires_at:
            return timezone.now() >= self.expires_at
        return False

    def get_absolute_short_url(self, request=None):
        if request:
            return request.build_absolute_uri(reverse('shortener_redirect', args=[self.slug]))
        return reverse('shortener_redirect', args=[self.slug])

class Click(models.Model):
    shorturl = models.ForeignKey(ShortURL, on_delete=models.CASCADE, related_name='clicks')
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.shorturl.slug} clicked at {self.timestamp}"
