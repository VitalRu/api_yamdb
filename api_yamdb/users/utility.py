from django.conf import settings
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """
    Генерирует JWT-токены для пользователя.
    """
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }


def send_code(token, email):
    """
    Отправляет код подтверждения на указанный email.
    """
    subject = 'Код подтверждения'
    message = f'Код - {token}'
    from_email = settings.EMAIL_ADDRESS
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
