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
from django.utils.encoding import force_text, escape_uri_path
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, FormView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from dateutil.relativedelta import relativedelta
from PIL import Image
from lib.convert import *
from rent_db.models import *


class LedgerView(TemplateView):
    """
    物件台帳表示
    """
    template_name = 'room/ledger.html'

    def __init__(self, **kwargs):
        self.user = None
        self.company = None
        self.room = None
        self.equipments = None
        self.building_image = None
        self.layout_image = None
        self.room_image = None

        super().__init__(**kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = self.request.user
        if not self.user:
            raise Http404

        self.company = Company.get_instance()

        oid = kwargs['oid']
        self.room = get_object_or_404(Room, oid=oid)
        self.room.building.auth_user = self.user

        if self.room:
            equipments = RoomEquipment.objects.filter(
                room=self.room,
                is_deleted=False,
            ).order_by('priority', 'equipment__category__priority', 'equipment__priority', 'id').all()

            for item in equipments:
                if not self.equipments:
                    self.equipments = ''
                else:
                    self.equipments += '・'
                self.equipments += item.equipment.name

            for item in self.room.building.pictures:
                if item.picture_type.is_building_exterior:
                    self.building_image = item
                    self.building_image.building.auth_user = self.user
                    break

            for item in self.room.pictures:
                if item.picture_type.is_layout:
                    self.layout_image = item
                    self.layout_image.room.building.auth_user = self.user
                    break

            for item in self.room.pictures:
                if item.picture_type.is_room and not item.picture_type.is_layout:
                    self.room_image = item
                    self.room_image.room.building.auth_user = self.user
                    break

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['company'] = self.company
        context['room'] = self.room
        context['equipments'] = self.equipments
        context['building_image'] = self.building_image
        context['layout_image'] = self.layout_image
        context['room_image'] = self.room_image
        context['condo_fees_name'] = settings.CONDO_FEES_NAME
        return context
