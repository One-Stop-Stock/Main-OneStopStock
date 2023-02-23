from django.shortcuts import render

from django.http import HttpResponse

def home_view(request, *args, **kwargs):
    print(request.user)
    return render(request, "home.html", {})

def tristen_a3p3(request, *args, **kwargs):
    return render(request, "tristena3p3.html", {})

def ryleya3p3(request, *args, **kwargs):
    return render(request, "ryleya3p3.html", {})	

def ryana3p3(request, *args, **kwargs):
    return render(request, "ryana3p3.html", {})	
