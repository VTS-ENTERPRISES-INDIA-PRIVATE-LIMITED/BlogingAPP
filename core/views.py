from django.shortcuts import render, redirect
from .forms import RegisterForm, UpdateProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from BlogApp.models import Blog
from .models import CustomUser, EmpID
from .serializers import EmpIDSerializer 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
import json
import os
from django.http import JsonResponse
from django.conf import settings
import logging

@api_view(['GET'])
def get_json_data(request):
    json_file_path = os.path.join(settings.BASE_DIR, 'emp_id_data.json')
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        return JsonResponse(data, safe=False)
    except FileNotFoundError:
        return JsonResponse({"error": "File not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Error decoding JSON"}, status=500)
valid_emp_ids=get_json_data


logger = logging.getLogger(__name__)

@api_view(['GET'])
def validate_emp_id(request):
    emp_id = request.GET.get('emp_id')
    logger.info(f"Received emp_id: {emp_id}")

    if not emp_id:
        return Response({"error": "emp_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    if EmpID.objects.filter(emp_id=emp_id).exists():
        return Response({"valid": True}, status=status.HTTP_200_OK)
    
    return Response({"valid": False}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("index")
    context = {'form': form, 'is_index_page': False, 'show_footer': False}
    return render(request, "core/signup.html", context)

def signin(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.warning(request, 'Invalid credentials')
            return redirect('signin')
    context = {'is_index_page': False, 'show_footer': False,}
    return render((request), "core/login.html", context)

def signout(request):
    logout(request)
    return redirect('index')

@login_required(login_url="signin")
def profile(request):
    user = request.user
    
    p_blogs = Blog.objects.filter(user=user, status='published')
    d_blogs = Blog.objects.filter(user=user, status='draft')

    context = {"user": user, "p_blogs": p_blogs,"d_blogs":d_blogs, 'is_index_page': False, 'show_footer': True,}
    return render(request, "core/profile.html", context)



@login_required(login_url="signin")
def update_profile(request):
    if request.user.is_authenticated:
        user = request.user
        form = UpdateProfileForm(instance=user)
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully")
                return redirect("profile")
    context = {"form": form, 'is_index_page': False, 'show_footer': True,}
    return render(request, "core/update_profile.html", context)


@api_view(['GET','POST','DELETE','PUT'])
def sample_api(request):
    if request.method=='GET':
        emp_id = EmpID.objects.all() 
        serializer = EmpIDSerializer(emp_id, many=True)
        return JsonResponse({'emp_id':serializer.data})
    if request.method=='POST':
        serializer = EmpIDSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)