from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    ROLES_USER = [
        (USER, 'User'),
        (ADMIN, 'Administrator'),
    ]
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        blank=False
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True,
        null=False
    )
    first_name = models.CharField(
        'first_name',
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        'last_name',
        max_length=150,
        blank=False
    )
    password = models.CharField(
        'password',
        max_length=150,
        blank=False
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=100,
        choices=ROLES_USER,
        default=USER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username'
    ]

    @property
    def is_admin(self) -> str:
        return self.role == self.ADMIN

    class Meta:
        ordering = ['id']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="username_is_not_me"
            )
        ]


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='Нельзя подписываться дважды',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='Нельзя подписываться на себя',
            )
        ]

    def __str__(self):
        return (
            f'{self.user.username} подписан на {self.author.username}'
        )
