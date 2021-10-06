"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from rest_framework import serializers
from api.models import MapSearchGarage
from .area_serializer import AreaSerializer
from .arrival_type_serializer import ArrivalTypeSerializer
from .building_type_serializer import BuildingTypeSerializer
from .city_serializer import CitySerializer
from .department_serializer import DepartmentSerializer
from .garage_status_serializer import GarageStatusSerializer
from .pref_serializer import PrefSerializer
from .station_serializer import StationSerializer
from .garage_picture_serializer import GaragePictureSerializer
from .tax_type_serializer import TaxTypeSerializer


class MapSearchGarageSerializer(serializers.ModelSerializer):
    """検索駐車場"""
    agency_department = DepartmentSerializer(many=False)
    area = AreaSerializer(many=False)
    arrival_type1 = ArrivalTypeSerializer(many=False)
    arrival_type2 = ArrivalTypeSerializer(many=False)
    arrival_type3 = ArrivalTypeSerializer(many=False)
    building_type = BuildingTypeSerializer(many=False)
    city = CitySerializer(many=False)
    department = DepartmentSerializer(many=False)
    garage_status = GarageStatusSerializer(many=False)
    garage_fee_tax_type = TaxTypeSerializer(many=False)
    pref = PrefSerializer(many=False)
    station1 = StationSerializer(many=False)
    station2 = StationSerializer(many=False)
    station3 = StationSerializer(many=False)

    garage_picture = GaragePictureSerializer(many=False)

    class Meta:
        model = MapSearchGarage
        fields = (
            'id',
            'oid',
            'garage_code',
            'garage_name',
            'garage_kana',
            'garage_old_name',
            'postal_code',
            'address',
            'pref',
            'city',
            'town_address',
            'town_name',
            'house_no',
            'lat',
            'lng',
            'area_text',
            'area',
            'department',
            'agency_department',
            'nearest_station1',
            'arrival_type1',
            'station1',
            'station_time1',
            'bus_stop1',
            'bus_stop_time1',
            'nearest_station2',
            'arrival_type2',
            'station2',
            'station_time2',
            'bus_stop2',
            'bus_stop_time2',
            'nearest_station3',
            'arrival_type3',
            'station3',
            'station_time3',
            'bus_stop3',
            'bus_stop_time3',
            'building_type_text',
            'building_type',
            'garage_status_text',
            'garage_status',
            'garage_fee_text',
            'garage_fee_lower',
            'garage_fee_upper',
            'garage_fee_tax_type',
            'web_catch_copy',
            'web_appeal',
            'garage_picture',
        )
