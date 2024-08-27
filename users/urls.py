from django.urls import path

from . import views
from .views import SignUpView
from .views import LoginView

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup_view, name="signup"),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]