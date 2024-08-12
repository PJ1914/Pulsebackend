from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
import os
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework import status
from .serializers import GeminiSerializer
import google.generativeai as genai
from google.cloud import vision
import io
import speech_recognition as sr

load_dotenv()

def index(request):
    return HttpResponse({'message': 'Hello, world! This is your Django app.'})

test_key = 'AIzaSyDGwSA4vpgACT1DzT7LBsuXryx5U3zNmGY'

class TestView(GenericViewSet):
    def post(self, request):
        return Response({"message": "hello world"})

genai.configure(api_key=test_key)

# Function to handle image recognition using Google's Vision API
def analyze_image(image_file):
    client = vision.ImageAnnotatorClient()

    with io.open(image_file, 'rb') as image:
        content = image.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    return [label.description for label in labels]

# Function to handle speech recognition using SpeechRecognition library
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Error with the speech recognition service: {e}"

class GeminiViewSet(APIView):
    def post(self, request):
        serializer = GeminiSerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data['message']
            chat_history = serializer.validated_data.get('chatHistory', [])

            # Handle image file
            image_file = request.FILES.get('image')
            image_labels = analyze_image(image_file) if image_file else []

            # Handle audio file
            audio_file = request.FILES.get('audio')
            audio_text = transcribe_audio(audio_file) if audio_file else ""

            try:
                model = genai.GenerativeModel("gemini-pro")
                chat = model.start_chat(history=chat_history)

                # Incorporate image labels and audio text into the prompt
                if image_labels:
                    prompt += f"\nImage contains: {', '.join(image_labels)}."
                if audio_text:
                    prompt += f"\nVoice command: {audio_text}."

                response = chat.send_message(prompt)

                return Response({'response': response.text}, status=status.HTTP_200_OK)
            except Exception as e:
                print(f'Error at line {e.__traceback__.tb_lineno}: {str(e)}')
                return Response({'error': f'Error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def main(request):
    # Replace with your logic for handling main route
    return HttpResponse({'message': 'Main route'})

def login(request):
    # Replace with your logic for handling login route
    return HttpResponse({'message': 'Login route'})

def logout(request):
    # Replace with your logic for handling logout route
    return HttpResponse({'message': 'Logout route'})
