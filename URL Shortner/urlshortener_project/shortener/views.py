# shortener/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils import timezone
from django.urls import reverse
from django.db import transaction

from .models import ShortURL, Click
from .forms import ShortURLCreateForm, ShortURLEditForm
from .utils import generate_slug_for, unique_slug_from_pk
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import FileResponse

# ---------- Auth views ----------
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'shortener/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'shortener/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# ---------- Home / Dashboard ----------
def home(request):
    if request.user.is_authenticated:
        return redirect('list_urls')
    return render(request, 'shortener/home.html')

# ---------- Create short URL ----------
@login_required
def create_shorturl(request):
    if request.method == 'POST':
        form = ShortURLCreateForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            custom_slug = form.cleaned_data.get('custom_slug') or None
            expires_at = form.cleaned_data.get('expires_at')
            with transaction.atomic():
                # create a placeholder ShortURL to get an id if not using custom
                if custom_slug:
                    obj = ShortURL.objects.create(
                        owner=request.user,
                        original_url=original_url,
                        slug=custom_slug,
                        expires_at=expires_at,
                        custom=True
                    )
                else:
                    # create with random slug first to reserve
                    temp_slug = generate_slug_for()
                    obj = ShortURL.objects.create(
                        owner=request.user,
                        original_url=original_url,
                        slug=temp_slug,
                        expires_at=expires_at,
                        custom=False
                    )
                    # now if you prefer base62 encoding of pk, update slug
                    obj.slug = unique_slug_from_pk(obj.pk)
                    # ensure uniqueness; if collision improbable but check
                    if ShortURL.objects.filter(slug=obj.slug).exclude(pk=obj.pk).exists():
                        # fallback random
                        obj.slug = generate_slug_for()
                    obj.save()
            return redirect('list_urls')
    else:
        form = ShortURLCreateForm()
    return render(request, 'shortener/create.html', {'form': form})

# ---------- List / Manage ----------
@login_required
def list_urls(request):
    urls = ShortURL.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'shortener/list.html', {'urls': urls})

@login_required
def edit_url(request, pk):
    obj = get_object_or_404(ShortURL, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ShortURLEditForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('list_urls')
    else:
        form = ShortURLEditForm(instance=obj)
    return render(request, 'shortener/edit.html', {'form': form, 'object': obj})

@login_required
def delete_url(request, pk):
    obj = get_object_or_404(ShortURL, pk=pk, owner=request.user)
    if request.method == 'POST':
        obj.delete()
        return redirect('list_urls')
    return render(request, 'shortener/delete_confirm.html', {'object': obj})

# ---------- Stats ----------
@login_required
def url_stats(request, pk):
    obj = get_object_or_404(ShortURL, pk=pk, owner=request.user)
    clicks = obj.clicks.order_by('-timestamp')[:200]  # last 200 clicks
    return render(request, 'shortener/stats.html', {'object': obj, 'clicks': clicks})

# ---------- QR code view ----------
@login_required
def qr_code_view(request, slug):
    obj = get_object_or_404(ShortURL, slug=slug, owner=request.user)
    # generate QR for the absolute short URL
    short_url = request.build_absolute_uri(reverse('shortener_redirect', args=[obj.slug]))
    img = qrcode.make(short_url)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return FileResponse(buf, as_attachment=False, filename=f'{obj.slug}.png')

# ---------- Redirect view ----------
def shortener_redirect(request, slug):
    obj = get_object_or_404(ShortURL, slug=slug)
    # check expiration
    if obj.is_expired():
        # show a simple page or do 410 Gone
        return render(request, 'shortener/expired.html', {'object': obj}, status=410)
    # increment click count and record click
    obj.click_count = obj.click_count + 1
    obj.save(update_fields=['click_count'])
    # create Click record
    ip = request.META.get('REMOTE_ADDR')
    ua = request.META.get('HTTP_USER_AGENT', '')
    Click.objects.create(shorturl=obj, ip_address=ip, user_agent=ua)
    return HttpResponseRedirect(obj.original_url)
