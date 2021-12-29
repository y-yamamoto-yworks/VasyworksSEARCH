"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.conf import settings
from django.test import Client
from django.urls import reverse
import warnings
from api.api_helper import ApiHelper
from rent_db.models import Company


class MapSearchNonResidentialViewSetTest(TestCase):
    """
    非居住用建物リストビューセットのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()
        self.company = Company.objects.get(pk=settings.COMPANY_ID)

    def test_get_view_set(self):
        url = reverse(
            'search_non_residential_buildings',
            args=[
                ApiHelper.get_key(),
            ],
        )
        url += "?north=35.049928&south=35.049926&east=135.76684&west=135.76682"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        building_list = response.data['list']
        self.assertEqual(building_list[0]['building_name'], '表示項目確認用マンション')

    def test_get_view_set_with_rent(self):
        url = reverse(
            'search_non_residential_buildings',
            args=[
                ApiHelper.get_key(),
            ],
        )
        url += "?north=35.049928&south=35.049926&east=135.76684&west=135.76682"
        url += "&l_rnt=100000&u_rnt=200000"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        building_list = response.data['list']
        self.assertEqual(building_list[0]['building_name'], '表示項目確認用マンション')

    def test_get_view_set_with_rent_no_data(self):
        url = reverse(
            'search_non_residential_buildings',
            args=[
                ApiHelper.get_key(),
            ],
        )
        url += "?north=35.049928&south=35.049926&east=135.76684&west=135.76682"
        url += "&l_rnt=50000&u_rnt=100000"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        list_count = response.data['count']
        self.assertEqual(list_count, 0)

    def test_get_view_set_with_room_area(self):
        url = reverse(
            'search_non_residential_buildings',
            args=[
                ApiHelper.get_key(),
            ],
        )
        url += "?north=35.049928&south=35.049926&east=135.76684&west=135.76682"
        url += "&l_ra=40&u_ra=50"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        building_list = response.data['list']
        self.assertEqual(building_list[0]['building_name'], '表示項目確認用マンション')

    def test_get_view_set_with_room_area_no_data(self):
        url = reverse(
            'search_non_residential_buildings',
            args=[
                ApiHelper.get_key(),
            ],
        )
        url += "?north=35.049928&south=35.049926&east=135.76684&west=135.76682"
        url += "&l_ra=20&u_ra=25"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        list_count = response.data['count']
        self.assertEqual(list_count, 0)

    def test_get_view_set_with_layout(self):
        url = reverse(
            'search_residential_buildings',
            args=[
                ApiHelper.get_key(),
            ],
        )
        url += "?north=35.049928&south=35.049926&east=135.76684&west=135.76682"
        url += "&lay=20,30"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        building_list = response.data['list']
        self.assertEqual(building_list[0]['building_name'], '表示項目確認用マンション')

    def test_get_view_set_with_layout_no_data(self):
        url = reverse(
            'search_residential_buildings',
            args=[
                ApiHelper.get_key(),
            ],
        )
        url += "?north=35.049928&south=35.049926&east=135.76684&west=135.76682"
        url += "&lay=10,20"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        list_count = response.data['count']
        self.assertEqual(list_count, 0)
