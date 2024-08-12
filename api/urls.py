# api/urls.py
from django.urls import path
from . import views2

urlpatterns = [


    # Separate paths for views2 to avoid conflict with 'home'
    path('api-index/', views2.index, name='api-index'),
    path('gemini/', views2.GeminiViewSet.as_view(), name='gemini'),
    path('main/', views2.main, name='main'),
    path('login/', views2.login, name='login'),
    path('logout/', views2.logout, name='logout'),
    path('test/', views2.TestView.as_view({"post": "post"})),



]
