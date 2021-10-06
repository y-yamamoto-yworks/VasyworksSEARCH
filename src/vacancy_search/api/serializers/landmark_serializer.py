"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from rest_framework import serializers
from rent_db.models import Landmark
from .landmark_type_serializer import LandmarkTypeSerializer


class LandmarkSerializer(serializers.ModelSerializer):
    landmark_type = LandmarkTypeSerializer(many=False)

    class Meta:
        model = Landmark
        fields = (
            'id',
            'name',
            'kana',
            'short_name',
            'lat',
            'lng',
            'priority',
            'landmark_type',
        )
