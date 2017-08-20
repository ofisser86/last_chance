# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render



# Journal views.

def journal(request):
    return render(request, 'students/journal.html', {})

