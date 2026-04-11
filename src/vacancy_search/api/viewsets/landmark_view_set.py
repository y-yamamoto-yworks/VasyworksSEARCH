"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2020 - 2026 Yasuhiro Yamamoto
"""
import urllib.parse
import django_filters
from django.shortcuts import render
from rest_framework import viewsets, filters
from django.db.models import Q
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str, escape_uri_path
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from lib.convert import *
from api.api_helper import ApiHelper
from rent_db.models import Landmark
from api.serializers import LandmarkSerializer


class LandmarkViewSet(viewsets.ModelViewSet):
    """
    ランドマーク
    """
    @method_decorator(login_required)
    def list(self, request, *args, **kwargs):
        key = kwargs.get('key')
        if not ApiHelper.check_key(key):
            raise Exception

        landmark_type_id = kwargs.get('landmark_type_id')

        self.queryset = Landmark.objects.filter(
            Q(landmark_type_id=landmark_type_id, is_stopped=False,) | Q(pk=0)
        ).order_by('landmark_type__priority', 'priority', 'kana').all()
        self.serializer_class = LandmarkSerializer

        return super().list(request, args, kwargs)
