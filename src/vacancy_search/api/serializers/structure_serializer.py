"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from rest_framework import serializers
from rent_db.models import Structure


class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = (
            'id',
            'idb64',
            'name',
        )
