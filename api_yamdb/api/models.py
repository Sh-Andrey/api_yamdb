from enum import Enum
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from .validators import validate_title_year


class Category(models.Model):
    name = models.CharField(
        max_length=60,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        unique=True,
        blank=True
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        max_length=60,
        verbose_name='Жанр'
    )
    slug = models.SlugField(
        unique=True,
        blank=True
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=60,
        verbose_name='Наименование'
    )

    year = models.IntegerField(validators=[validate_title_year],
                               verbose_name='Год премьеры', blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='titles',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Наименование'
        verbose_name_plural = 'Наименования'

    def __str__(self):
        return self.name


class Role(Enum):
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER = 'user'

    def __str__(self):
        return str(self.value)

    @classmethod
    def choices(cls):
        return tuple((role.value, role.name.lower()) for role in cls)


class User(AbstractUser):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False,
                          verbose_name='ID'),
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        choices=Role.choices(),
        default=Role.USER,
        max_length=255)

    bio = models.CharField(
        verbose_name='Описание',
        max_length=50,
        help_text='Описание',
        blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return str(self.email)

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR.value

    @property
    def is_admin(self):
        return self.role == Role.ADMIN.value


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'review'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'), name='unique_pair'
            ),
        )

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'comment'

    def __str__(self):
        return self.text
