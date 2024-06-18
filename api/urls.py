# api/urls.py

from django.urls import path
from .views import  wish_me, take_command, get_weather, search_wikipedia, tell_joke,home
from . import views2

# router = DefaultRouter()
# router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', home, name='home'),

    path('wish/', wish_me, name='wish_me'),
    path('command/', take_command, name='take_command'),
    path('weather/<str:location>/', get_weather, name='get_weather'),
    path('wiki/<str:query>/', search_wikipedia, name='search_wikipedia'),
    path('joke/', tell_joke, name='tell_joke'),
    path('', views2.index, name='index'),
    path('gemini/', views2.GeminiViewSet.as_view(), name='gemini'),
    path('main/', views2.main, name='index'),
    path('login/', views2.login, name='login'),
    path('logout/', views2.logout, name='logout'),
    path ("test/", views2.TestView.as_view({"post":"post"}))
    # Add more URL patterns as needed
]
