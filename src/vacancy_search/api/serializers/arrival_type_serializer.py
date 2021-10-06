"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from rest_framework import serializers
from rent_db.models import ArrivalType


class ArrivalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrivalType
        fields = (
            'id',
            'idb64',
            'name',
        )
