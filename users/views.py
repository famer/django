from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from .forms import SignUpForm


# Create your views here.

def signup_view(request):
    return HttpResponse("WIP")
    form = SignUpForm()
    return render(request, "users/signup.html", {
        "form": form
    })

def index(request):
    ...

def login_view(request):
    ...

def logout_view(request):
    ...