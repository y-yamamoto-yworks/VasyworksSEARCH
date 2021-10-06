"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from .models import User


class UserBackEnd(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password)

        if user:
            if not user.is_company and not user.is_company_admin:
                return None

        return user
