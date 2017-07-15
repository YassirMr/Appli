from django.shortcuts import render
from django.template import loader
from . import forms

def index(request):  #take this one off after
    return render(request, 'doe/index.html')

def exp1(request):
    return render(request,'doe/exp1.html')

def result1(request):
    return render(request, 'doe/result1.html')

def Introduction(request):
    return render(request, 'doe/Introduction.html')