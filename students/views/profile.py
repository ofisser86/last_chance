# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from ..models.students import Student
from ..models.groups import Group


def students_profile(request, sid):
    return render(request, 'students/profile.html', {})
