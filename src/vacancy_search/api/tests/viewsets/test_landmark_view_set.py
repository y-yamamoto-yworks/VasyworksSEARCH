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


class LandmarkViewSetTest(TestCase):
    """
    ランドマークビューセットのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()

    def test_get_landmark_view_set(self):
        url = reverse(
            'api_landmarks',
            args=[
                ApiHelper.get_key(),
                '10',        # 大学
            ],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        area = response.data[0]
        self.assertEqual(area['name'], '京都大学')
