"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
import urllib.parse
import django_filters
from django.shortcuts import render
from rest_framework import viewsets, filters
from django.db.models import Q
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text, escape_uri_path
from lib.convert import *
from api.api_helper import ApiHelper
from rent_db.models import Station
from api.serializers import StationSerializer


class StationViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        key = kwargs.get('key')
        if not ApiHelper.check_key(key):
            raise Exception

        railway_id = kwargs.get('railway_id')

        self.queryset = Station.objects.filter(
            Q(railway_id=railway_id, is_trading=True, is_stopped=False) | Q(pk=0)
        ).order_by('priority').all()
        self.serializer_class = StationSerializer

        return super().list(request, args, kwargs)
