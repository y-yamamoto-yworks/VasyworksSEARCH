"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group, Permission
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from rent_db.models import Staff
from lib.convert import *
from lib.functions import *


class User(AbstractBaseUser, PermissionsMixin):
    """
    ユーザ
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        db_column='username',
        max_length=150,
        unique=True,
        db_index=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), db_column='first_name', max_length=30, null=True, blank=True)
    last_name = models.CharField(_('last name'), db_column='last_name', max_length=150, null=True, blank=True)

    staff = models.ForeignKey(
        Staff,
        db_column='staff_id',
        related_name='users',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    
    email = models.EmailField(_('email address'), db_column='email', null=True, blank=True)
    is_company = models.BooleanField(_('is_company'), db_column='is_company', default=False)
    is_company_admin = models.BooleanField(_('is_company_admin'), db_column='is_company_admin', default=False)
    is_staff = models.BooleanField(_('staff status'), db_column='is_staff', default=False)
    is_active = models.BooleanField(_('active'), db_column='is_active', default=True)
    date_joined = models.DateTimeField(_('date joined'), db_column='date_joined', default=timezone.now)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='user_set',
        related_query_name='user',
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        managed = False
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def idb64(self):
        return base64_decode_id(self.pk)

    @property
    def full_name(self):
        return self.get_full_name()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
