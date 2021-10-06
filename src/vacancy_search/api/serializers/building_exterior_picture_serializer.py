"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from rest_framework import serializers
from lib.serializer_helper import SerializerHelper
from api.models import BuildingExteriorPicture
from .picture_type_serializer import PictureTypeSerializer


class BuildingExteriorPictureSerializer(serializers.ModelSerializer):
    """検索建物の外観写真"""
    picture_type = PictureTypeSerializer(many=False)

    class Meta:
        model = BuildingExteriorPicture
        fields = SerializerHelper.get_building_picture_fields()
