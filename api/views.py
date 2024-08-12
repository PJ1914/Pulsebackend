from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import wikipedia
import requests
import os
from google.cloud import vision

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def home(request):
    return HttpResponse("Hello, world!")

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
    
    speak(greeting)
    return JsonResponse({'message': greeting})

def search_wikipedia(request, query):
    try:
        results = wikipedia.summary(query, sentences=2)
        response = f"According to Wikipedia: {results}"
    except Exception:
        response = "Sorry, I couldn't find information on Wikipedia."
    speak(response)
    return JsonResponse({'summary': response})

def tell_joke(request):
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Parallel lines have so much in common. It's a shame they'll never meet."
    ]
    joke = random.choice(jokes)
    speak(joke)
    return JsonResponse({'joke': joke})

@csrf_exempt
def text_detection_view(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        image_path = f"temp/{image.name}"
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        result = text_detection(image_path)
        os.remove(image_path)
        return JsonResponse({"text": result})
    return HttpResponseBadRequest("Invalid request")

@csrf_exempt
def face_recognition_view(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        image_path = f"temp/{image.name}"
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        result = face_recognition_from_image(image_path)
        os.remove(image_path)
        return JsonResponse({"face_locations": result})
    return HttpResponseBadRequest("Invalid request")

@csrf_exempt
def label_image_view(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        image_path = f"temp/{image.name}"
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        result = label_image(image_path)
        os.remove(image_path)
        return JsonResponse({"labels": result})
    return HttpResponseBadRequest("Invalid request")

@csrf_exempt
def detect_objects_view(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        image_path = f"temp/{image.name}"
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        result = detect_objects(image_path)
        os.remove(image_path)
        return JsonResponse({"objects": result})
    return HttpResponseBadRequest("Invalid request")

@csrf_exempt
def identify_language_view(request):
    if request.method == 'POST':
        data = JsonResponse.loads(request.body)
        text = data.get('text', '')
        result = identify_language(text)
        return JsonResponse({"language": result})
    return HttpResponseBadRequest("Invalid request")

@csrf_exempt
def detect_landmark_view(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        image_path = f"temp/{image.name}"
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        result = detect_landmark(image_path)
        os.remove(image_path)
        return JsonResponse({"landmarks": result})
    return HttpResponseBadRequest("Invalid request")

def text_detection(image_path):
    """Detects text from an image using Google Vision API."""
    try:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path_to_your_google_credentials.json'
        client = vision.ImageAnnotatorClient()
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        return texts[0].description if texts else "No text detected"
    except Exception as e:
        return f"Error in text detection: {e}"

def face_recognition_from_image(image_path):
    """Placeholder function for face recognition."""
    # Since the import is removed, this is a placeholder.
    return "Face recognition functionality not implemented."

def label_image(image_path):
    """Labels objects in an image using Google Vision API."""
    try:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path_to_your_google_credentials.json'
        client = vision.ImageAnnotatorClient()
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        return [label.description for label in labels]
    except Exception as e:
        return f"Error in image labeling: {e}"

def detect_objects(image_path):
    """Placeholder function for object detection."""
    # Since OpenCV imports are removed, this is a placeholder.
    return "Object detection functionality not implemented."

def identify_language(text):
    """Placeholder function for language identification."""
    # Since the import is removed, this is a placeholder.
    return "Language identification functionality not implemented."

def detect_landmark(image_path):
    """Detects landmarks in an image using Google Vision API."""
    try:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path_to_your_google_credentials.json'
        client = vision.ImageAnnotatorClient()
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.landmark_detection(image=image)
        landmarks = response.landmark_annotations
        return [landmark.description for landmark in landmarks]
    except Exception as e:
        return f"Error in landmark detection: {e}"
