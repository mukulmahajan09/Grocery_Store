# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import models

def store_home(request):
    return render(request, 'index.html')