"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from django.urls import include, path
from django.views.generic import TemplateView
from search_map.views import *

urlpatterns = [
    path('residential/', ResidentialSearchMapIndexView.as_view(), name='search_map_residential_index'),
    path('non_residential/', NonResidentialSearchMapIndexView.as_view(), name='search_map_non_residential_index'),
    path('garage/', GarageSearchMapIndexView.as_view(), name='search_map_garage_index'),

    path('residential/map/', ResidentialSearchMapView.as_view(), name='search_map_residential_map'),
    path('non_residential/map/', NonResidentialSearchMapView.as_view(), name='search_map_non_residential_map'),
    path('garage/map/', GarageSearchMapView.as_view(), name='search_map_garage_map'),

    path('', TemplateView.as_view(template_name='404.html'), name='search_map_index'),
]
