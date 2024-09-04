import secrets
import random
import string

from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm, UserRecoveryPasswordForm
from users.models import User

from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    """
    Класс-контроллер для регистрации пользователя.
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Создает и направляет пользователю на эл. почту токен для верификации эл. почты.
        :param:
        token - генерация токена,
        host - host пользователя, пользователь определяется через request, host через get_host(),
        url - ссылка (путь перехода) пользователю для подтверждения эл. почты,
        send_mail() - функция отправки пользователю на эл. почту.
        """
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение адреса электронной почты',
            message=f'Перейдите по ссылке для подтверждение адреса электронной почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """
    Верификация эл. почты пользователя после перехода по ссылке, отправленной через form_valid().
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class ProfileView(UpdateView):
    """
    Класс-контроллер для редактирования профиля пользователя.
    """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """
        Метод для получения объекта класса (пользователя) для его редактирования.
        """
        return self.request.user


class UserRecoveryPasswordView(PasswordResetView):
    """
    Класс-контроллер для восстановления пароля.
    """
    model = User
    form_class = UserRecoveryPasswordForm
    template_name = 'users/recovery_password_form.html'
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        if self.request.method == 'POST':
            user_email = self.request.POST['email']
            try:
                user = User.objects.get(email=user_email)
                new_password = ''.join([random.choice(string.digits + string.ascii_letters) for _ in range(0, 10)])
                user.set_password(new_password)
                user.save()
                send_mail(
                    subject='Восстановление пароля',
                    message=f'Для входа используйте новый пароль: {new_password}',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
            except User.DoesNotExist:
                form.add_error(None, User.DoesNotExist(f"Пользователь {user_email} не найден"))
                return self.render_to_response(self.get_context_data(form=form))

        return redirect(reverse('users:login'))
