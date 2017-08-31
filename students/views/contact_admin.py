# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def contact_admin(request):
    return render(request, 'contact_admin/contact_admin.html', {})

