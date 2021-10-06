"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from rest_framework import serializers
from rent_db.models import Station
from .railway_serializer import RailwaySerializer


class StationSerializer(serializers.ModelSerializer):
    railway = RailwaySerializer(many=False)

    class Meta:
        model = Station
        fields = (
            'id',
            'idb64',
            'name',
            'railway',
        )
