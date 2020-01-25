from django.shortcuts import render, redirect


# Create your views here.

#for redirect to dashboard
def index(request):
    return render(request , 'home.html',{})

#the dashboard page
def dashboard(request):
    return render(request , 'dashboard.html' , {})
