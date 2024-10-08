from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .forms import SignUpForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from .tasks import send_email
import logging 

logger = logging.getLogger('itjobs')

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'registration/signup.html'

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info(f'User { user.username } registered')

            # email confirmation 
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_email.delay(mail_subject, message, to_email, html=True)
            return render(request, "users/base.html", {
                "title": "подтвердите email",
                "text": "Подтвердите Ваш email для завершения регистрации"
            })
            # email confirmation end
        
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


User = get_user_model()

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, "users/after_registration.html", {
                "title": "подтверждение регистрации",
        })
    else:
        return HttpResponse('Activation link is invalid!')


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
        return render(request, "users/login.html", {
            "form": form
        })

    

def logout_view(request):
    logout(request)
    return redirect("users:login")