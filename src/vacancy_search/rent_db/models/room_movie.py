"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from lib.convert import *
from lib.functions import *
from lib.cache_file_helper import CacheFileHelper
from .movie_type import MovieType


class RoomMovie(models.Model):
    """
    部屋動画
    """
    id = models.AutoField(_('id'), db_column='id', primary_key=True)

    building = models.ForeignKey(
        'Building',
        db_column='building_id',
        related_name='room_movies',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    room = models.ForeignKey(
        'Room',
        db_column='room_id',
        related_name='room_movies',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )

    file_name = models.CharField(_('file_name'), db_column='file_name', max_length=255)
    cache_name = models.CharField(_('cache_name'), db_column='cache_name', max_length=255)
    movie_type = models.ForeignKey(
        MovieType,
        db_column='movie_type_id',
        related_name='room_movies',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    is_publish_web = models.BooleanField(_('is_publish_web'), db_column='is_publish_web', db_index=True, default=True)
    is_publish_vacancy = models.BooleanField(_('is_publish_vacancy'), db_column='is_publish_vacancy', db_index=True, default=True)
    comment = models.CharField(_('comment'), db_column='comment', max_length=50, null=True, blank=True)
    note = models.CharField(_('note'), db_column='note', max_length=255, null=True, blank=True)
    priority = models.IntegerField(_('priority'), db_column='priority', db_index=True, default=100)

    is_deleted = models.BooleanField(_('is_deleted'), db_column='is_deleted', db_index=True, default=False)

    class Meta:
        managed = False
        db_table = 'room_movie'
        ordering = ['priority', 'id']
        verbose_name = _('room_movie')
        verbose_name_plural = _('room_movies')

    @property
    def idb64(self):
        return base64_decode_id(self.pk)

    @property
    def cache_file_url(self):
        """キャッシュファイルのURLの取得"""
        url = None

        auth_user = self.room.building.auth_user
        if auth_user:
            url = CacheFileHelper.get_property_movie_file_url(
                self.room.building.file_oid,
                self.file_name,
                self.cache_name,
            )

        return url
