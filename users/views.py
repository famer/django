from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from .forms import SignUpForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


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
    form = AuthenticationForm()
    return render(request, "registration/login.html", {
        "form": form
    })

def logout_view(request):
    ...