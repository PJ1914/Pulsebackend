# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  wish_me, take_command, get_weather, search_wikipedia, tell_joke,home

# router = DefaultRouter()
# router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', home, name='home'),

    path('wish/', wish_me, name='wish_me'),
    path('command/', take_command, name='take_command'),
    path('weather/<str:location>/', get_weather, name='get_weather'),
    path('wiki/<str:query>/', search_wikipedia, name='search_wikipedia'),
    path('joke/', tell_joke, name='tell_joke'),
    # Add more URL patterns as needed
]
