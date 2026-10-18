"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2020 - 2026 Yasuhiro Yamamoto
"""
from django.urls import include, path
from django.views.generic import TemplateView
from api.viewsets import *

urlpatterns = [
    path('areas/<int:city_id>', AreaViewSet.as_view({'get': 'list'}), name='api_areas'),
    path('building_types/', BuildingTypeViewSet.as_view({'get': 'list'}), name='api_building_types'),
    path('cities/<int:pref_id>', CityViewSet.as_view({'get': 'list'}), name='api_cities'),
    path('landmark_types/', LandmarkTypeViewSet.as_view({'get': 'list'}), name='api_landmark_types'),
    path('landmarks/<int:landmark_type_id>', LandmarkViewSet.as_view({'get': 'list'}), name='api_landmarks'),
    path('prefs/', PrefViewSet.as_view({'get': 'list'}), name='api_prefs'),
    path('railways/', RailwayViewSet.as_view({'get': 'list'}), name='api_railways'),
    path('stations/<int:railway_id>', StationViewSet.as_view({'get': 'list'}), name='api_stations'),

    path('garages/', MapSearchGarageViewSet.as_view({'get': 'list'}), name='search_garages'),
    path('non_residential_buildings/', MapSearchNonResidentialViewSet.as_view({'get': 'list'}), name='search_non_residential_buildings'),
    path('residential_buildings/', MapSearchResidentialViewSet.as_view({'get': 'list'}), name='search_residential_buildings'),

]