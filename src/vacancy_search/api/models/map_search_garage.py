"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from django.conf import settings
from django.db import models
from django.db.models import Q, Subquery, OuterRef
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from lib.convert import *
from lib.functions import *
from lib.data_helper import DataHelper
from rent_db.models import *
from .map_search_garage_conditions import MapSearchGarageConditions
from .garage_picture import GaragePicture


class MapSearchGarage(models.Model):
    """駐車場リスト（月極駐車場の建物リスト）"""
    id = models.AutoField(_('id'), db_column='id', primary_key=True)
    oid = models.CharField(_('oid'), db_column='oid', db_index=True, unique=True, max_length=50)
    garage_code = models.CharField(_('garage_code'), db_column='garage_code', max_length=20, db_index=True, null=True, blank=True)
    garage_name = models.CharField(_('garage_name'), db_column='garage_name', max_length=100, db_index=True, null=True, blank=True)
    garage_kana = models.CharField(_('garage_kana'), db_column='garage_kana', max_length=100, db_index=True, null=True, blank=True)
    garage_old_name = models.CharField(_('garage_old_name'), db_column='garage_old_name', max_length=100, null=True, blank=True)

    postal_code = models.CharField(_('postal_code'), db_column='postal_code', max_length=10, null=True, blank=True)
    pref = models.ForeignKey(
        Pref,
        db_column='pref_id',
        related_name='searched_garages',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_trading_area=True) | Q(pk=0),
    )
    city = models.ForeignKey(
        City,
        db_column='city_id',
        related_name='searched_garages',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_trading_area=True, is_stopped=False) | Q(pk=0),
    )
    town_address = models.CharField(_('town_address'), db_column='town_address', max_length=255, null=True, blank=True)
    town_name = models.CharField(_('town_name'), db_column='town_name', max_length=100, null=True, blank=True)
    house_no = models.CharField(_('house_no'), db_column='house_no', max_length=100, null=True, blank=True)
    lat = models.FloatField(_('lat'), db_column='lat', db_index=True, default=0)
    lng = models.FloatField(_('lng'), db_column='lng', db_index=True, default=0)
    area = models.ForeignKey(
        Area,
        db_column='area_id',
        related_name='searched_garages',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_stopped=False) | Q(pk=0),
    )
    department = models.ForeignKey(
        Department,
        db_column='department_id',
        related_name='searched_garages',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_stopped=False, is_deleted=False) | Q(pk=0),
    )
    priority_level = models.IntegerField(_('priority_level'), db_column='priority_level', db_index=True, default=50)
    agency_department = models.ForeignKey(
        Department,
        db_column='agency_department_id',
        related_name='agency_searched_garages',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_stopped=False, is_deleted=False) | Q(pk=0),
    )
    arrival_type1 = models.ForeignKey(
        ArrivalType,
        db_column='arrival_type_id1',
        related_name='searched_garages1',
        on_delete=models.PROTECT,
        default=0,
    )
    station1 = models.ForeignKey(
        Station,
        db_column='station_id1',
        related_name='searched_garages1',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_trading=True, is_stopped=False) | Q(pk=0),
    )
    station_time1 = models.IntegerField(_('station_time1'), db_column='station_time1', default=0)
    bus_stop1 = models.CharField(_('bus_stop1'), db_column='bus_stop1', max_length=50, null=True, blank=True)
    bus_stop_time1 = models.IntegerField(_('bus_stop_time1'), db_column='bus_stop_time1', default=0)

    arrival_type2 = models.ForeignKey(
        ArrivalType,
        db_column='arrival_type_id2',
        related_name='searched_garages2',
        on_delete=models.PROTECT,
        default=0,
    )
    station2 = models.ForeignKey(
        Station,
        db_column='station_id2',
        related_name='searched_garages2',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_trading=True, is_stopped=False) | Q(pk=0),
    )
    station_time2 = models.IntegerField(_('station_time2'), db_column='station_time2', default=0)
    bus_stop2 = models.CharField(_('bus_stop2'), db_column='bus_stop2', max_length=50, null=True, blank=True)
    bus_stop_time2 = models.IntegerField(_('bus_stop_time2'), db_column='bus_stop_time2', default=0)

    arrival_type3 = models.ForeignKey(
        ArrivalType,
        db_column='arrival_type_id3',
        related_name='searched_garages3',
        on_delete=models.PROTECT,
        default=0,
    )
    station3 = models.ForeignKey(
        Station,
        db_column='station_id3',
        related_name='searched_garages3',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
        limit_choices_to=Q(is_trading=True, is_stopped=False) | Q(pk=0),
    )
    station_time3 = models.IntegerField(_('station_time3'), db_column='station_time3', default=0)
    bus_stop3 = models.CharField(_('bus_stop3'), db_column='bus_stop3', max_length=50, null=True, blank=True)
    bus_stop_time3 = models.IntegerField(_('bus_stop_time3'), db_column='bus_stop_time3', default=0)

    building_type = models.ForeignKey(
        BuildingType,
        db_column='building_type_id',
        related_name='searched_garages',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    garage_status = models.ForeignKey(
        GarageStatus,
        db_column='garage_status_id',
        related_name='searched_garages',
        db_index=True,
        on_delete=models.PROTECT,
        default=0,
    )
    garage_fee_lower = models.IntegerField(_('garage_fee_lower'), db_column='garage_fee_lower', default=0)
    garage_fee_upper = models.IntegerField(_('garage_fee_upper'), db_column='garage_fee_upper', default=0)
    garage_fee_tax_type = models.ForeignKey(
        TaxType,
        db_column='garage_fee_tax_type_id',
        related_name='searched_garages',
        on_delete=models.PROTECT,
        default=0,
    )
    web_catch_copy = models.CharField(_('web_catch_copy'), db_column='web_catch_copy', max_length=100, null=True, blank=True)
    web_appeal = models.CharField(_('web_appeal'), db_column='web_appeal', max_length=255, null=True, blank=True)
    garage_fee = models.CharField(_('garage_fee'), db_column='garage_fee', max_length=255, null=True, blank=True)

    class Meta:
        managed = False

    """
    検索関連
    """
    @classmethod
    def get_garages(cls, conditions: MapSearchGarageConditions):
        """クエリセットの取得"""
        params = {}

        sql = 'SELECT {0} FROM {1} WHERE {2} ORDER BY {3};'.format(
            cls.__get_sql_columns(),
            cls.__get_sql_tables(conditions=conditions, params=params),
            cls.__get_sql_conditions(conditions=conditions, params=params),
            cls.__get_sql_orders(),
        )

        ans = cls.objects.raw(raw_query=sql, params=params)

        return ans

    """
    SQL関連内部メソッド
    """
    @classmethod
    def __get_sql_columns(cls):
        """SQLのカラム一覧"""
        ans = 'building.id'
        ans += ', building.oid'
        ans += ', building.building_code AS garage_code'
        ans += ', building.building_name AS garage_name'
        ans += ', building.building_kana AS garage_kana'
        ans += ', building.building_old_name AS garage_old_name'
        ans += ', building.postal_code'
        ans += ', building.pref_id'
        ans += ', building.city_id'
        ans += ', building.town_address'
        ans += ', building.town_name'
        ans += ', building.house_no'
        ans += ', building.lat'
        ans += ', building.lng'
        ans += ', building.area_id'
        ans += ', building.department_id'
        ans += ', building.agency_department_id'
        ans += ', building.arrival_type_id1'
        ans += ', building.station_id1'
        ans += ', building.station_time1'
        ans += ', building.bus_stop1'
        ans += ', building.bus_stop_time1'
        ans += ', building.arrival_type_id2'
        ans += ', building.station_id2'
        ans += ', building.station_time2'
        ans += ', building.bus_stop2'
        ans += ', building.bus_stop_time2'
        ans += ', building.arrival_type_id3'
        ans += ', building.station_id3'
        ans += ', building.station_time3'
        ans += ', building.bus_stop3'
        ans += ', building.bus_stop_time3'
        ans += ', building.building_type_id'
        ans += ', building.garage_status_id'
        ans += ', building.garage_fee_lower'
        ans += ', building.garage_fee_upper'
        ans += ', building.garage_fee_tax_type_id'
        ans += ', building.web_catch_copy'
        ans += ', building.web_appeal'

        return ans

    @classmethod
    def __get_sql_tables(cls, conditions: MapSearchGarageConditions, params):
        """SQLのテーブル一覧"""
        ans = 'building'
        ans += ' INNER JOIN building_type ON building.building_type_id = building_type.id'
        ans += ' AND building_type.id = 310'        # 月極駐車場（建物の駐車場種別は参照しない）
        ans += ' INNER JOIN pref ON building.pref_id = pref.id'
        ans += ' INNER JOIN city ON building.city_id = city.id'

        if conditions:
            # 管理種別の限定有無
            ans += xstr(conditions.get_only_own_property_sql())

        return ans

    @classmethod
    def __get_sql_conditions(cls, conditions: MapSearchGarageConditions, params):
        """SQLの建物用条件一覧"""
        ans = 'building.is_deleted = FALSE'
        if conditions:
            ans += cls.__and_condition_sql(conditions.get_latlng_sql(params=params), ans)
            ans += cls.__and_condition_sql(conditions.get_only_for_rent_sql(), ans)
            ans += cls.__and_condition_sql(conditions.get_garage_fee_sql(params=params), ans)

        return ans

    @classmethod
    def __and_condition_sql(cls, condition_sql, sql):
        """SQL文字列に条件SQLをAND条件で追加"""
        ans = ''
        if xstr(condition_sql):
            if xstr(sql) != '':
                ans += " AND "
            ans += xstr(condition_sql)
        return ans


    @classmethod
    def __get_sql_orders(cls):
        """SQLの並び順一覧"""
        ans = 'building.priority_level DESC'
        ans += ', pref.priority, city.priority, building.building_kana'
        return ans

    """
    プロパティ
    """
    @property
    def garage_picture(self):
        return GaragePicture.get_picture(self.id)

    """
    表示用プロパティ
    """
    @property
    def address(self):
        return DataHelper.get_address_text(
            self.pref,
            self.city,
            self.town_address,
            self.house_no,
            None)

    @property
    def area_text(self):
        return DataHelper.get_area_text(self.area)

    @property
    def nearest_station1(self):
        return DataHelper.get_nearest_station_text(
            self.arrival_type1,
            self.station1,
            self.station_time1,
            self.bus_stop1,
            self.bus_stop_time1)

    @property
    def nearest_station2(self):
        return DataHelper.get_nearest_station_text(
            self.arrival_type2,
            self.station2,
            self.station_time2,
            self.bus_stop2,
            self.bus_stop_time2)

    @property
    def nearest_station3(self):
        return DataHelper.get_nearest_station_text(
            self.arrival_type3,
            self.station3,
            self.station_time3,
            self.bus_stop3,
            self.bus_stop_time3)

    @property
    def building_type_text(self):
        return DataHelper.get_building_type_text(
            self.building_type)

    @property
    def garage_status_text(self):
        return DataHelper.get_garage_status_text(self.garage_status)

    @property
    def garage_fee_text(self):
        return DataHelper.get_building_garage_fee_text(
            GarageType.objects.get(pk=1),     # 有料扱い
            self.garage_fee_lower,
            self.garage_fee_upper,
            self.garage_fee_tax_type)
