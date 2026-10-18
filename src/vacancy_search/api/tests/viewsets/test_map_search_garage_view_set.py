"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2020 - 2026 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.conf import settings
from django.test import Client
from django.urls import reverse
import warnings
from api.api_helper import ApiHelper
from rent_db.models import Company


class MapSearchGarageViewSetTest(TestCase):
    """
    月極駐車場リストビューセットのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()
        self.company = Company.objects.get(pk=settings.COMPANY_ID)

        response = self.client.post(
            reverse('login'),
            {'username': 't-kanri', 'password': 'guest1234'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_get_view_set(self):
        url = reverse(
            'search_garages',
        )
        url += "?north=34.99556&south=34.99557&east=135.75928&west=135.75931"
        response = self.client.get(url, HTTP_X_API_KEY=ApiHelper.get_key())
        self.assertEqual(response.status_code, 200)
        building_list = response.data['list']
        self.assertEqual(building_list[0]['garage_name'], 'サンプルガレージ01')

        response_invalid = self.client.get(url, HTTP_X_API_KEY='AABBCCDDEEFF')
        self.assertEqual(response_invalid.status_code, 403)

    def test_get_view_set_with_rent(self):
        url = reverse(
            'search_garages',
        )
        url += "?north=34.99556&south=34.99557&east=135.75928&west=135.75931"
        url += "&l_fee=5000&u_fee=20000"
        response = self.client.get(url, HTTP_X_API_KEY=ApiHelper.get_key())
        self.assertEqual(response.status_code, 200)
        building_list = response.data['list']
        self.assertEqual(building_list[0]['garage_name'], 'サンプルガレージ01')

        response_invalid = self.client.get(url, HTTP_X_API_KEY='AABBCCDDEEFF')
        self.assertEqual(response_invalid.status_code, 403)

    def test_get_view_set_with_rent_no_data(self):
        url = reverse(
            'search_garages',
        )
        url += "?north=34.99556&south=34.99557&east=135.75928&west=135.75931"
        url += "&u_fee=5000"
        response = self.client.get(url, HTTP_X_API_KEY=ApiHelper.get_key())
        self.assertEqual(response.status_code, 200)
        list_count = response.data['count']
        self.assertEqual(list_count, 0)

        response_invalid = self.client.get(url, HTTP_X_API_KEY='AABBCCDDEEFF')
        self.assertEqual(response_invalid.status_code, 403)
