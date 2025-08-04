from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        TEACHER = 'teacher', 'Teacher'
        ADMIN = 'admin', 'Admin'

    username = None
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT
    )

    def is_student(self):
        return self.role == self.Role.STUDENT

    def is_teacher(self):
        return self.role == self.Role.TEACHER

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
