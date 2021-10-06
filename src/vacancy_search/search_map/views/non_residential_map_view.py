"""
System Name: Vasyworks
Project Name: vacancy_search
Encoding: UTF-8
Copyright (C) 2021 Yasuhiro Yamamoto
"""
import os
import datetime
import uuid
from abc import ABCMeta, abstractmethod
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text, escape_uri_path
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, FormView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from dateutil.relativedelta import relativedelta
from PIL import Image
from lib.convert import *
from api.api_helper import ApiHelper
from rent_db.models import Company


class NonResidentialSearchMapView(TemplateView):
    """
    非居住用地図検索
    """
    template_name = 'search_map/non_residential_map.html'

    def __init__(self, **kwargs):
        self.user = None
        self.company = None

        self.lat = settings.DEFAULT_LAT
        self.lng = settings.DEFAULT_LNG

        super().__init__(**kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        if not self.user:
            raise Http404

        self.company = Company.get_instance()

        if request.method == 'GET':
            data = self.request.GET.get('lat', None)
            if data:
                self.lat = xfloat(data)

            data = self.request.GET.get('lng', None)
            if data:
                self.lng = xfloat(data)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['company'] = self.company
        context['api_key'] = ApiHelper.get_key()
        context['lat'] = self.lat
        context['lng'] = self.lng
        return context
