"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
import os
import datetime
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from lib.convert import *
from lib.functions import *
from .pref import Pref


class JuniorHighSchool(models.Model):
    """
    中学校区
    """
    id = models.IntegerField(_('id'), db_column='id', primary_key=True)

    pref = models.ForeignKey(
        Pref,
        db_column='pref_id',
        related_name='pref_junior_high_schools',
        db_index=True,
        on_delete=models.PROTECT,
    )

    name = models.CharField(_('name'), db_column='name', max_length=50)
    kana = models.CharField(_('kana'), db_column='kana', db_index=True, max_length=100, null=True, blank=True)
    lat = models.FloatField(_('lat'), db_column='lat', db_index=True, default=0)
    lng = models.FloatField(_('lng'), db_column='lng', db_index=True, default=0)
    is_stopped = models.BooleanField(_('is_stopped'), db_column='is_stopped', db_index=True, default=False)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'junior_high_school'
        ordering = ['pref_id', 'kana', 'id']
        verbose_name = _('junior_high_school')
        verbose_name_plural = _('junior_high_schools')

    @property
    def idb64(self):
        return base64_decode_id(self.pk)
