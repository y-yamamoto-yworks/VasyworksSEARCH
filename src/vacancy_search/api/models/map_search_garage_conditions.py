"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
import datetime
from django.conf import settings
from lib.convert import *
from lib.functions import *
from lib.url_param_helper import UrlParamHelper


class MapSearchGarageConditions(object):
    """駐車場検索条件"""
    def __init__(self, *args, **kwargs):
        self.only_own_property = False  # 自社物件のみ
        self.only_for_rent = True    # 募集中物件のみ
        self.north = None  # 北緯
        self.south = None  # 南緯
        self.east = None  # 東経
        self.west = None  # 西経

        self.garage_fee_lower = None  # 駐車料下限
        self.garage_fee_upper = None  # 駐車料上限

        super().__init__(*args, **kwargs)

    """
    メソッド
    """
    def set_conditions(self, url_params):
        """URLパラメータ（クエリストリング）の条件設定"""
        self.only_own_property = UrlParamHelper.get_bool_param('only_own', url_params)     # 自社物件のみ
        self.only_for_rent = UrlParamHelper.get_bool_param('for_rent', url_params)     # 募集中物件のみ
        self.north = UrlParamHelper.get_float_param('north', url_params)      # 北緯
        self.south = UrlParamHelper.get_float_param('south', url_params)      # 南緯
        self.east = UrlParamHelper.get_float_param('east', url_params)      # 東経
        self.west = UrlParamHelper.get_float_param('west', url_params)      # 西経
        self.garage_fee_lower = UrlParamHelper.get_int_param('l_fee', url_params)     # 駐車料下限
        self.garage_fee_upper = UrlParamHelper.get_int_param('u_fee', url_params)      # 駐車料上限

    """
    プロパティ
    """
    @property
    def latlng_is_valid(self):
        """有効な緯度経度条件の確認"""
        ans = False
        if 0 < xfloat(self.south) < xfloat(self.north) and 0 < xfloat(self.west) < xfloat(self.east):
            ans = True
        return ans

    """
    FROM句用SQL
    """
    def get_only_own_property_sql(self):
        ans = None
        if self.only_own_property:
            ans = ' INNER JOIN management_type ON building.management_type_id = management_type.id'
            ans += ' AND ('
            ans += 'management_type.is_own = TRUE'
            ans += ' OR management_type.is_entrusted = TRUE'
            ans += ')'

        return ans

    """
    WHERE句用SQL
    """
    def get_latlng_sql(self, params):
        """緯度経度（東西南北）"""
        ans = None
        if self.latlng_is_valid:
            ans = 'building.lat > %(south)s'
            ans += ' AND building.lat < %(north)s'
            ans += ' AND building.lng > %(west)s'
            ans += ' AND building.lng < %(east)s'
            params['south'] = self.south
            params['north'] = self.north
            params['west'] = self.west
            params['east'] = self.east
        return ans

    def get_only_for_rent_sql(self):
        """募集中のみ"""
        ans = None
        if self.only_for_rent:
            ans = 'building.garage_status_id IN (1, 3, 4)'  # 空き有・要確認・別参照

        return ans

    def get_garage_fee_sql(self, params):
        """駐車料"""
        ans = None
        if xint(self.garage_fee_upper) > 0:
            # 上限は税込（tax_id:2）を考慮する。
            ans = '((building.garage_fee_lower <= %(garage_fee_upper)s AND building.garage_fee_tax_type_id != 2)'
            ans += ' OR (building.garage_fee_lower <= %(garage_fee_upper_including_tax)s AND building.garage_fee_tax_type_id = 2))'
            params['garage_fee_upper'] = xint(self.garage_fee_upper)
            params['garage_fee_upper_including_tax'] = xint(xint(self.garage_fee_upper) * (1 + settings.TAX_RATE))
        if xint(self.garage_fee_lower) > 0:
            if ans:
                ans += ' AND '
            ans = '(building.garage_fee_lower >= %(garage_fee_lower)s'
            ans += ' OR building.garage_fee_upper >= %(garage_fee_lower)s)'
            params['garage_fee_lower'] = xint(self.garage_fee_lower)
        return ans

    """
    内部メソッド
    """
    @classmethod
    def __get_id_targets(cls, id_name, id_list, params):
        ans = ''
        if id_list:
            count = 0
            for item in id_list:
                param_name = '{0}_{1}'.format(id_name, count)
                if ans != '':
                    ans += ','
                ans += '%({0})s'.format(param_name)
                params[param_name] = item
                count += 1
        return ans
