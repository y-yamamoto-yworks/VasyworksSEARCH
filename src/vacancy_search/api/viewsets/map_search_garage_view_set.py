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
from api.pagination import *
from api.models import *
from api.serializers import MapSearchGarageSerializer


class MapSearchGarageViewSet(viewsets.ReadOnlyModelViewSet):
    """月極駐車場リスト"""
    pagination_class = ListApiPagination
    conditions = None

    def list(self, request, *args, **kwargs):
        key = kwargs.get('key')
        if not ApiHelper.check_key(key):
            raise Exception

        self.conditions = MapSearchGarageConditions()
        self.conditions.set_conditions(self.request.query_params)

        self.queryset = MapSearchGarage.get_garages(
            conditions=self.conditions,
        )
        self.serializer_class = MapSearchGarageSerializer

        return super().list(request, args, kwargs)
