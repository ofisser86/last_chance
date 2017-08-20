# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render


# Groups views.
def groups_list(request):
    return render(request, 'students/groups.html', {})


def groups_add(request):
    return HttpResponse('<h1> Groups Add Form </h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1> Groups %s Editing </h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1> Groups deleting %s</h1>' % gid)