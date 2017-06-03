from django.shortcuts import render
from django.template import loader
from . import forms

def index(request):

    return render(request, 'doe/index.html')

def exp1(request):
    return render(request,'doe/exp1.html')