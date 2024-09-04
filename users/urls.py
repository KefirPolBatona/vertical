from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import never_cache

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, email_verification, UserRecoveryPasswordView

app_name = UsersConfig.name


urlpatterns = [
    path('', never_cache(LoginView.as_view(template_name='users/login.html')), name='login'),
    path('logout/', never_cache(LogoutView.as_view()), name='logout'),
    path('register/', never_cache(RegisterView.as_view()), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('recovery-password/', never_cache(UserRecoveryPasswordView.as_view()), name='recovery_password'),
]
