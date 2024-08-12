# api/urls.py
from django.urls import path
from .views import (
    wish_me, take_command, get_weather, search_wikipedia, tell_joke, home,
    text_detection_view, face_recognition_view, label_image_view, detect_objects_view,
    identify_language_view, detect_landmark_view
)
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
