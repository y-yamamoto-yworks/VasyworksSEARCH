"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from django.urls import include, path
from django.views.generic import TemplateView
from api.viewsets import *

urlpatterns = [
    path('areas/<str:key>/<int:city_id>', AreaViewSet.as_view({'get': 'list'}), name='api_areas'),
    path('building_types/<str:key>/', BuildingTypeViewSet.as_view({'get': 'list'}), name='api_building_types'),
    path('cities/<str:key>/<int:pref_id>', CityViewSet.as_view({'get': 'list'}), name='api_cities'),
    path('landmark_types/<str:key>/', LandmarkTypeViewSet.as_view({'get': 'list'}), name='api_landmark_types'),
    path('landmarks/<str:key>/<int:landmark_type_id>', LandmarkViewSet.as_view({'get': 'list'}), name='api_landmarks'),
    path('prefs/<str:key>/', PrefViewSet.as_view({'get': 'list'}), name='api_prefs'),
    path('railways/<str:key>/', RailwayViewSet.as_view({'get': 'list'}), name='api_railways'),
    path('stations/<str:key>/<int:railway_id>', StationViewSet.as_view({'get': 'list'}), name='api_stations'),

    path('garages/<str:key>/', MapSearchGarageViewSet.as_view({'get': 'list'}), name='search_garages'),
    path('non_residential_buildings/<str:key>/', MapSearchNonResidentialViewSet.as_view({'get': 'list'}), name='search_non_residential_buildings'),
    path('residential_buildings/<str:key>/', MapSearchResidentialViewSet.as_view({'get': 'list'}), name='search_residential_buildings'),

]