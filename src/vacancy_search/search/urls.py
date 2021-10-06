"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from django.urls import include, path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('building_code/', SearchBuildingCodeView.as_view(), name='search_building_code'),
    path('building_id/', SearchBuildingIdView.as_view(), name='search_building_id'),
    path('building_name/', SearchBuildingNameView.as_view(), name='search_building_name'),

    path('', TemplateView.as_view(template_name='404.html'), name='search_index'),
]
