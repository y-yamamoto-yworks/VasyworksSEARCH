"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
from rest_framework import pagination
from rest_framework.response import Response


class ListApiPagination(pagination.LimitOffsetPagination):
    """リスト用ページネーション"""
    default_limit = 20

    def get_paginated_response(self, data):
        return Response({
            'count': self.count,
            'limit': self.limit,
            'offset': self.offset,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'list': data
        })
