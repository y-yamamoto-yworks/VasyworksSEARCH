"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.test import Client
from django.urls import reverse
import warnings
from api.api_helper import ApiHelper


class StationViewSetTest(TestCase):
    """
    駅ビューセットのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()

    def test_get_station_view_set(self):
        url = reverse(
            'api_stations',
            args=[
                ApiHelper.get_key(),
                '70',        # 地下鉄烏丸線
            ],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        area = response.data[0]
        self.assertEqual(area['name'], '国際会館')
