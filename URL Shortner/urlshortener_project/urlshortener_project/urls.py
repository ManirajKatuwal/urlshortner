# urlshortener_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shortener import views as short_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shortener.urls')),  # app handles index & redirect
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
