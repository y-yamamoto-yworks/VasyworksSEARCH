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
        self.assertEqual(ApiHelper.get_key(), 'f7e815ad8b88969d48a2e43f81e0b1aee28523f9f1330e345cc172747cc811d02ec6531855dece38dbe3692104c34c67')

    def test_check_key(self):
        self.assertTrue(ApiHelper.check_key('f7e815ad8b88969d48a2e43f81e0b1aee28523f9f1330e345cc172747cc811d02ec6531855dece38dbe3692104c34c67'))
