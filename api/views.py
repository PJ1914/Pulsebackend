# backend/api/views.py
from django.http import JsonResponse, HttpResponse
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import cv2
import requests
from bs4 import BeautifulSoup
import random
from django.views import View



# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def home(request):
    return HttpResponse("heeloo world")
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wish_me(request):
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Speak the greeting
    engine.say(greeting)
    engine.runAndWait()
    
    # Stop the TTS engine
    engine.stop()
    
    return JsonResponse({'message': greeting})

def take_command(request):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 2
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return JsonResponse({'error': "Sorry, I didn't catch that. Can you please repeat?"})
    except sr.RequestError:
        return JsonResponse({'error': "Sorry, I'm unable to access the Google API at the moment."})

    return JsonResponse({'query': query.lower()})

def get_weather(request, location):
    url = f"https://www.weather.com/en-IN/weather/today/l/{location}"
    headers = {
        "User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        temp = soup.find('div', class_='today_nowcard-temp').get_text()
        condition = soup.find('div', class_='today_nowcard-phrase').get_text()
        response = f"The current temperature in {location} is {temp} and the weather condition is {condition}."
    except AttributeError:
        response = "Sorry, I couldn't retrieve the weather information for that location."
    speak(response)
    return JsonResponse({'weather': response})

def search_wikipedia(request, query):
    try:
        results = wikipedia.summary(query, sentences=2)
        response = f"According to Wikipedia: {results}"
    except Exception:
        response = "Sorry, I couldn't find information on Wikipedia."
    speak(response)
    return JsonResponse({'summary': response})

def tell_joke(request):
    jokes = ["Why don't scientists trust atoms? Because they make up everything!",
             "I told my wife she was drawing her eyebrows too high. She looked surprised.",
             "Why did the scarecrow win an award? Because he was outstanding in his field!",
             "Parallel lines have so much in common. It's a shame they'll never meet."]
    joke = random.choice(jokes)
    
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Speak the joke
    engine.say(joke)
    engine.runAndWait()
    
    # Stop the TTS engine
    engine.stop()
    
    return JsonResponse({'joke': joke})

class WeatherView(View):
    def get(self, request, location):
        url = f"https://www.weather.com/en-IN/weather/today/l/{location}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        try:
            temp = soup.find('div', class_='today_nowcard-temp').get_text()
            condition = soup.find('div', class_='today_nowcard-phrase').get_text()
            return JsonResponse({
                'temperature': temp,
                'condition': condition
            })
        except AttributeError:
            return JsonResponse({'error': 'Could not retrieve weather data'}, status=500)



