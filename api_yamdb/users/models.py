from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Абстрактная модель пользователя, расширяющая модель AbstractUser из Django.
    """
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = (
        (ADMIN, 'ADMIN'),
        (MODERATOR, 'MODERATOR'),
        (USER, 'USER'),
    )
    email = models.EmailField(max_length=50, unique=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        default='user'
    )

    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['id']
        verbose_name = "user"
        verbose_name_plural = "users"

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def get_full_name(self):
        """
        Возвращает полное имя пользователя.
        """
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        """
        Возвращает короткое имя пользователя.
        """
        return self.first_name

    def __str__(self):
        return self.username
