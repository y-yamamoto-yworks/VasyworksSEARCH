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


class SearchBuildingCodeViewTest(TestCase):
    """
    建物コード検索ビューのテスト
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

    def test_get_search_name_building_list_view(self):
        url = reverse('search_building_code')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_post_search_name_building_list_view(self):
        url = reverse('search_building_code')
        response = self.client.post(
            url,
            {
                'building_code': 'Y001',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        building = response.context['buildings'][0]
        self.assertEqual(building.building_name, 'サンプルマンション')
