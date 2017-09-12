# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView


class JournalView(TemplateView):
    template_name = 'students/journal.html'
