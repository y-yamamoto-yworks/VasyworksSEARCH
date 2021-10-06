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
from api.serializers import MapSearchBuildingSerializer


class MapSearchNonResidentialViewSet(viewsets.ReadOnlyModelViewSet):
    """非居住用建物リスト"""
    pagination_class = ListApiPagination
    conditions = None

    def list(self, request, *args, **kwargs):
        key = kwargs.get('key')
        if not ApiHelper.check_key(key):
            raise Exception

        self.conditions = MapSearchConditions()
        self.conditions.set_conditions(self.request.query_params)

        self.queryset = MapSearchBuilding.get_buildings(
            conditions=self.conditions,
            is_residential=False,
        )
        self.serializer_class = MapSearchBuildingSerializer

        return super().list(request, args, kwargs)

    def paginate_queryset(self, queryset):
        """建物インスタンスに設定"""
        items = super().paginate_queryset(queryset)
        for item in items:
            item.conditions = self.conditions
            item.is_residential = False
        return items
