import uuid
import datetime

from django.core.validators import validate_email
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.db import models
from django.utils.translation import gettext_lazy as _


class MyAccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of username.
    """

    def create_user(self, email: str, username: str = None, password: str = None, is_active: bool = False):
        """
        Create and save a User with the given email, first name, last name and password.
        """
        if password is None:
            raise ValueError("User must have a password.")

        if not email:
            raise ValueError("User must have an email address.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.is_admin = False
        user.is_superuser = False
        user.is_staff = False
        user.is_active = is_active
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str = None, username: str = None, password: str = None):
        if password is None:
            raise ValueError('Superuser must have a password.')

        if email is None:
            raise ValueError('Superuser must have an email address.')

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('Username'),
        max_length=50,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
    )
    email = models.EmailField(
        _('email'),
        max_length=255,
        unique=True,
        validators=[validate_email],
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,   # can login
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    date_joined = models.DateField(_('Date Joined'), default=datetime.date.today)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username

    def get_email(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

