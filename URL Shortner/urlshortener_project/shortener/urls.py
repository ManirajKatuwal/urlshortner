# shortener/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # dashboard if logged in else landing
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_shorturl, name='create_shorturl'),
    path('my-urls/', views.list_urls, name='list_urls'),
    path('edit/<int:pk>/', views.edit_url, name='edit_url'),
    path('delete/<int:pk>/', views.delete_url, name='delete_url'),
    path('stats/<int:pk>/', views.url_stats, name='url_stats'),
    path('qr/<slug:slug>/', views.qr_code_view, name='qr_code_view'),
    path('r/<slug:slug>/', views.shortener_redirect, name='shortener_redirect'),  # redirect endpoint
]
