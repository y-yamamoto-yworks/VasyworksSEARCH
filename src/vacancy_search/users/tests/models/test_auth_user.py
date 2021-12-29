"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.db import transaction
from users.models import User
import warnings


class UserModelTest(TestCase):
    """
    ユーザモデルのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.user = User.objects.get(username='t-kanri')

        if transaction.get_autocommit():
            transaction.set_autocommit(False)

    def tearDown(self):
        transaction.rollback()

    def test_full_name(self):
        self.assertEqual(self.user.full_name, '管理 太郎')

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), '管理 太郎')

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), '太郎')
