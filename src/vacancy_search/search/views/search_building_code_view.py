"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
import os
import datetime
from abc import ABCMeta, abstractmethod
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, FormView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from dateutil.relativedelta import relativedelta
from PIL import Image
from lib.convert import *
from rent_db.models import Building
from search.forms import SearchBuildingCodeForm


class SearchBuildingCodeView(FormView):
    """
    建物コード検索
    """
    form_class = SearchBuildingCodeForm
    template_name = 'search/search_building_code.html'

    def __init__(self, **kwargs):
        self.user = None
        self.building_code = None
        self.is_searched = False

        super().__init__(**kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        if not self.user:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['is_searched'] = self.is_searched
        context['searched_building_code'] = self.building_code

        buildings = None
        if self.building_code:
            conditions = Q(is_deleted=False)
            conditions.add(Q(building_code=self.building_code), Q.AND)

            buildings = Building.objects.filter(conditions).order_by(
                'building_kana',
                'id',
            ).all()
        context['buildings'] = buildings

        return context

    def form_valid(self, form):
        if self.request.method in ('POST', 'PUT'):
            if form.data['building_code']:
                self.building_code = form.data['building_code']

            self.is_searched = True

        return self.render_to_response(self.get_context_data())

