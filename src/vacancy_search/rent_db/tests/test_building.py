"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.db import transaction
from rent_db.models import Building
from rent_db.models import Pref, City, Area
from users.models import User
import warnings


class BuildingModelTest(TestCase):
    """
    建物モデルのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.building = Building.objects.get(pk=2)      # 表示項目確認用マンション

        if transaction.get_autocommit():
            transaction.set_autocommit(False)

    def tearDown(self):
        transaction.rollback()

    def test_building_all_rooms(self):
        self.building.auth_user = User.objects.get(username='t-kanri')
        room = self.building.all_rooms.first()
        self.assertEqual(room.room_no, 'DEMO1')

    def test_building_facilities(self):
        facility = self.building.facilities.first()
        self.assertEqual(facility.facility_name, 'コンビニDEMO')

    def test_building_garages(self):
        garage = self.building.garages.first()
        self.assertEqual(garage.garage_name, 'DEMO01')

    def test_building_landmarks(self):
        landmark = self.building.landmarks.first()
        self.assertEqual(landmark.landmark.name, '京都府立大学')

    def test_building_files(self):
        file = self.building.files.first()
        self.assertEqual(file.file_title, '建物ファイルDEMO1')

    def test_building_movies(self):
        movie = self.building.movies.first()
        self.assertEqual(movie.movie_type.name, '屋内スペース')

    def test_building_panoramas(self):
        panorama = self.building.panoramas.first()
        self.assertEqual(panorama.panorama_type.name, 'エントランス')

    def test_building_pictures(self):
        picture = self.building.pictures.first()
        self.assertEqual(picture.picture_type.name, '建物外観')

    def test_building_address(self):
        self.assertEqual(self.building.address, '京都府京都市上京区住所町域DEMO町番地DEMOデータ A棟')
        self.building.building_no = None
        self.assertEqual(self.building.address, '京都府京都市上京区住所町域DEMO町番地DEMOデータ')

    def test_area_text(self):
        self.assertEqual(self.building.area_text, '今出川')

    def test_building_nearest_stations(self):
        self.assertEqual(self.building.nearest_station1, '地下鉄烏丸線 北大路駅まで徒歩5分')
        self.building.station1_id = 0
        self.assertIsNone(self.building.nearest_station1)

        self.assertEqual(self.building.nearest_station2, '地下鉄烏丸線 鞍馬口駅までバス10分（バス停 北大路バスターミナルまで徒歩5分）')
        self.building.station2_id = 0
        self.assertIsNone(self.building.nearest_station2)

        self.assertEqual(self.building.nearest_station3, '京福電鉄北野線 北野白梅町駅までバス15分（バス停 北大路バスターミナルまで徒歩5分）')
        self.building.station3_id = 0
        self.assertIsNone(self.building.nearest_station3)

    def test_building_type_text(self):
        self.assertEqual(self.building.building_type_text, 'アパート（建物種別DEMOデータ）')

    def test_build_year_month(self):
        self.assertEqual(self.building.build_year_month, '1995年3月築')

    def test_structure_text(self):
        self.assertEqual(self.building.structure_text, '軽量鉄骨造（建物構造DEMOデータ）')

    def test_elementary_school_text(self):
        self.assertEqual(self.building.elementary_school_text, '新町')

    def test_elementary_school_distance_text(self):
        self.assertEqual(self.building.elementary_school_distance_text, '100m')

    def test_junior_high_school_text(self):
        self.assertEqual(self.building.junior_high_school_text, '上京')

    def test_junior_high_school_distance_text(self):
        self.assertEqual(self.building.junior_high_school_distance_text, '200m')

    def test_garage_status_text(self):
        self.assertIsNone(self.building.garage_status_text)
        old_type_id = self.building.garage_type_id
        self.building.garage_type_id = 1
        self.assertEqual(self.building.garage_status_text, '要確認')
        self.building.garage_type_id = old_type_id

    def test_garage_distance_text(self):
        self.assertEqual(self.building.garage_distance_text, '100m')

    def test_garage_fee_text(self):
        self.assertIsNone(self.building.garage_fee_text)
        old_type_id = self.building.garage_type_id
        self.building.garage_type_id = 1
        self.building.garage_fee_lower = 12000
        self.building.garage_fee_upper = 15000
        self.building.garage_fee_tax_type_id = 1
        self.assertEqual(self.building.garage_fee_text, '12,000円 ～ 15,000円（税別）')
        self.building.garage_type_id = old_type_id

    def test_garage_charge_text(self):
        self.assertEqual(self.building.garage_charge_text, '4,000円 ～ 6,000円（税別）')

    def test_bike_parking_type_text(self):
        self.assertEqual(self.building.bike_parking_type_text, '原付可（有料）')

    def test_bike_parking_roof_text(self):
        self.assertEqual(self.building.bike_parking_roof_text, '屋根付き')

    def test_bike_parking_fee_text(self):
        self.assertEqual(self.building.bike_parking_fee_text, '300円 ～ 1,000円（税別）')

    def test_department_name_text(self):
        self.assertEqual(self.building.department_name_text, 'ワイワークス不動産 賃貸管理部')

    def test_department_tel_text(self):
        self.assertEqual(self.building.department_tel_text, '999-999-9999')

    def test_staff1_text(self):
        self.assertEqual(self.building.staff1_text, 'DEMO（賃貸管理部）')

    def test_staff2_text(self):
        self.assertEqual(self.building.staff2_text, '管理（賃貸管理部）')

    def test_register_text(self):
        self.assertEqual(self.building.register_text, '登記番号:9999999999 / 登記地番:登記所在地DEMO町999番地（家屋番号:999番） / 登記名義人:DEMO登記名義人')

    def test_agreement_existence_text(self):
        self.assertEqual(self.building.agreement_existence_text, '有り')

    def test_vacancy_recommend_comment(self):
        self.assertEqual(self.building.vacancy_recommend_comment, '空室情報キャッチコピーDEMOデータ')

    def test_trader_name_text(self):
        self.assertIsNone(self.building.trader_name_text)

    def test_trader_tel_text(self):
        self.assertIsNone(self.building.trader_tel_text)

    def test_owner_name_text(self):
        self.assertEqual(self.building.owner_name_text, 'DEMOオーナー')

    def test_owner_tel_text(self):
        self.assertEqual(self.building.owner_tel_text, '000-000-0000')
