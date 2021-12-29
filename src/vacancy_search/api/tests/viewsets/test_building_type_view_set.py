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


class BuildingTypeViewSetTest(TestCase):
    """
    建物種別ビューセットのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()

    def test_get_building_type_view_set(self):
        url = reverse(
            'api_building_types',
            args=[
                ApiHelper.get_key(),
            ],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        pref = response.data[0]
        self.assertEqual(pref['name'], 'マンション')
