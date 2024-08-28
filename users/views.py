from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .forms import SignUpForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'registration/signup.html'

# Create your views here.

def signup_view(request):
    return HttpResponse("WIP")
    form = SignUpForm()
    return render(request, "users/signup.html", {
        "form": form
    })

def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, "users/index.html", {
            "username": username
        })
    else:
        return HttpResponse('Hello, Guest!')


def login_view(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Вход пользователя в систему
            return redirect('users:index')  # Перенаправление на домашнюю страницу или другую страницу
        else:
            return HttpResponse("Invalid credentials")
    else:
        form = AuthenticationForm()
        return render(request, "registration/login.html", {
            "form": form
        })

    

def logout_view(request):
    logout(request)
    return redirect("users:login")