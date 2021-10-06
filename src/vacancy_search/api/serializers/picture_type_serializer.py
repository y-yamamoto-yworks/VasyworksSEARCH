"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from rest_framework import serializers
from rent_db.models import PictureType


class PictureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureType
        fields = (
            'id',
            'idb64',
            'name',
        )
