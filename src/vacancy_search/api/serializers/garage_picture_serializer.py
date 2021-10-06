"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from rest_framework import serializers
from lib.serializer_helper import SerializerHelper
from api.models import GaragePicture


class GaragePictureSerializer(serializers.ModelSerializer):
    """検索建物の外観写真"""
    class Meta:
        model = GaragePicture
        fields = (
            'id',
            'idb64',
            'building_oid',
            'thumbnail_file_url',
            'small_file_url',
            'medium_file_url',
            'large_file_url',
            'comment',
        )
