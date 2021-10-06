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
    path('<str:oid>', BuildingView.as_view(), name='building_building'),
    path('garages/<str:oid>', BuildingGarageListView.as_view(), name='building_garage_list'),

    path('', TemplateView.as_view(template_name='404.html'), name='building_index'),
]
