"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from django.urls import include, path
from django.views.generic import TemplateView
from .views import MenuIndexView

urlpatterns = [
    path('', MenuIndexView.as_view(), name='menu_index'),
]
