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


class GarageViewTest(TestCase):
    """
    月極駐車場ビューのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()

        response = self.client.post(
            reverse('login'),
            {'username': 't-kanri', 'password': 'guest1234', },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_get_building_view(self):
        url = reverse(
            'garage_garage',
            args=['f5145f0f1eb1476abd410c4b36eb956c'],     # サンプルガレージ01
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        garage = response.context['garage']
        self.assertEqual(garage.building_name, 'サンプルガレージ01')
