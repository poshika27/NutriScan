from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, ScannedFood

def landing(request):
    return render(request, 'users/landing.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import UserProfile
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        age = request.POST['age']
        height = float(request.POST['height'])
        weight = float(request.POST['weight'])
        gender = request.POST['gender']
        activity_level = request.POST['activity_level']
        medical_conditions = request.POST.getlist('medical_conditions')
        other_condition = request.POST.get('other_condition', '')

        if other_condition:
            medical_conditions.append(other_condition)

        
        bmi = round(weight / ((height / 100) ** 2), 2)

        try:
            user = User.objects.create_user(username=username, password=password)
            user_profile = UserProfile.objects.create(
                user=user,
                age=age,
                height=height,
                weight=weight,
                bmi=bmi,
                gender=gender,
                activity_level=activity_level,
                medical_conditions=", ".join(medical_conditions)  
            )
            user.save()
            user_profile.save()

            messages.success(request, "Registration successful. Please log in!")
            return redirect('login')
        except:
            messages.error(request, "Username already exists or error in registration.")
    
    return render(request, 'users/register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"🎉 Welcome back, {username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "🚫 Invalid username or password")

    return render(request, 'users/login.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'users/dashboard.html', {'profile': profile})

def leftover_view(request):
    return render(request, 'users/leftover.html')

def recipe(request):
    return render(request, 'users/recipe.html')

def cravings_view(request):
    return render(request, 'users/cravings.html')
def bmi_view(request):
    return render(request, 'users/bmi.html')

def user_logout(request):
    logout(request)
    messages.success(request, "🔓 You have been logged out.")
    return redirect('landing')

import pytesseract
from PIL import Image
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile  
from .ai_utils import get_ai_suggestion 



import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import pytesseract
from .ai_utils import get_ai_suggestion  
@csrf_exempt
def extract_text(request):
    if request.method == "POST":
        
        if request.FILES.get("image"):
            image_file = request.FILES["image"]
            image = Image.open(image_file)
            extracted_text = pytesseract.image_to_string(image)
        
        
        elif request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                extracted_text = data.get("text", "")
            except json.JSONDecodeError:
                return JsonResponse({"success": False, "message": "Invalid JSON data."})

        else:
            return JsonResponse({"success": False, "message": "No image or text data provided."})

        
        if request.user.is_authenticated:
            user = request.user
            user_data = {
                "age": user.age,
                "gender": user.gender,
                "bmi": user.bmi,
                "health_issues": user.health_issues,
            }
        else:
            user_data = {}

        
        ai_suggestion = get_ai_suggestion(extracted_text, user_data)

        return JsonResponse({"success": True, "text": extracted_text, "suggestion": ai_suggestion})
    
    return JsonResponse({"success": False, "message": "Invalid request method."})

from .ai_utils import get_ai_suggestion

@csrf_exempt
def extract_text(request):
    if request.method == "POST":
        
        if request.FILES.get("image"):
            image_file = request.FILES["image"]
            image = Image.open(image_file)
            extracted_text = pytesseract.image_to_string(image)
        
        
        elif request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                extracted_text = data.get("text", "")
            except json.JSONDecodeError:
                return JsonResponse({"success": False, "message": "Invalid JSON data."})

        else:
            return JsonResponse({"success": False, "message": "No image or text data provided."})

        # Send the extracted text to Gemini API or another service for suggestions
        if request.user.is_authenticated:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            user_data = {
                "age": user_profile.age,
                "gender": user_profile.gender,
                "bmi": user_profile.bmi,
                "health_issues": user_profile.medical_conditions,
            }
        else:
            user_data = {}

        ai_suggestion = get_ai_suggestion(extracted_text, user_data)

        # Return extracted text and suggestion to frontend
        return JsonResponse({
            "success": True, 
            "text": extracted_text, 
            "suggestion": ai_suggestion
        })
    
    return JsonResponse({"success": False, "message": "Invalid request method."})
