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


class ApiHelperTest(TestCase):
    """
    APIヘルパーのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()

    def test_get_key(self):
        self.assertEqual(ApiHelper.get_key(), 'd3f001762f51e18a0241bde03544d91cdcf0efb154b792d739ccfa36e1138577520af5a81240ceca')

    def test_check_key(self):
        self.assertTrue(ApiHelper.check_key('d3f001762f51e18a0241bde03544d91cdcf0efb154b792d739ccfa36e1138577520af5a81240ceca'))
