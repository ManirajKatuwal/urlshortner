# shortener/forms.py
from django import forms
from .models import ShortURL
from django.utils import timezone

class ShortURLCreateForm(forms.ModelForm):
    custom_slug = forms.CharField(required=False, max_length=100,
                                 help_text="Optional: choose your own short slug (letters/numbers/-, _).")
    expires_at = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = ShortURL
        fields = ['original_url']

    def clean_custom_slug(self):
        slug = self.cleaned_data.get('custom_slug', '').strip()
        if slug:
            #validation
            import re
            if not re.match(r'^[A-Za-z0-9\-_]+$', slug):
                raise forms.ValidationError("Slug may only contain letters, numbers, hyphens and underscores.")
            if ShortURL.objects.filter(slug=slug).exists():
                raise forms.ValidationError("That slug is already taken.")
        return slug

    def clean_expires_at(self):
        expires_at = self.cleaned_data.get('expires_at')
        if expires_at and expires_at <= timezone.now():
            raise forms.ValidationError("Expiration must be in the future.")
        return expires_at

class ShortURLEditForm(forms.ModelForm):
    expires_at = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = ShortURL
        fields = ['original_url', 'expires_at']
