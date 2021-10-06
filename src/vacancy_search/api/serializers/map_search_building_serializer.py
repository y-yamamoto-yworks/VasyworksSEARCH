"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from rest_framework import serializers
from api.models import MapSearchBuilding
from .area_serializer import AreaSerializer
from .arrival_type_serializer import ArrivalTypeSerializer
from .bike_parking_type_serializer import BikeParkingTypeSerializer
from .building_type_serializer import BuildingTypeSerializer
from .city_serializer import CitySerializer
from .department_serializer import DepartmentSerializer
from .garage_type_serializer import GarageTypeSerializer
from .pref_serializer import PrefSerializer
from .station_serializer import StationSerializer
from .structure_serializer import StructureSerializer
from .building_exterior_picture_serializer import BuildingExteriorPictureSerializer


class MapSearchBuildingSerializer(serializers.ModelSerializer):
    """検索建物"""
    agency_department = DepartmentSerializer(many=False)
    area = AreaSerializer(many=False)
    arrival_type1 = ArrivalTypeSerializer(many=False)
    arrival_type2 = ArrivalTypeSerializer(many=False)
    arrival_type3 = ArrivalTypeSerializer(many=False)
    bike_parking_type = BikeParkingTypeSerializer(many=False)
    building_type = BuildingTypeSerializer(many=False)
    city = CitySerializer(many=False)
    department = DepartmentSerializer(many=False)
    garage_type = GarageTypeSerializer(many=False)
    pref = PrefSerializer(many=False)
    station1 = StationSerializer(many=False)
    station2 = StationSerializer(many=False)
    station3 = StationSerializer(many=False)
    structure = StructureSerializer(many=False)

    exterior_picture = BuildingExteriorPictureSerializer(many=False)

    class Meta:
        model = MapSearchBuilding
        fields = (
            'id',
            'oid',
            'building_code',
            'building_name',
            'building_kana',
            'building_old_name',
            'postal_code',
            'address',
            'pref',
            'city',
            'town_address',
            'town_name',
            'house_no',
            'building_no',
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
            'structure_text',
            'structure',
            'building_rooms',
            'building_floors',
            'building_undergrounds',
            'build_year_month',
            'build_year',
            'build_month',
            'bike_parking_type_text',
            'bike_parking_type',
            'garage_type_text',
            'garage_type',
            'web_catch_copy',
            'web_appeal',
            'exterior_picture',
            'layout',
            'rent',
            'room_area',
        )
