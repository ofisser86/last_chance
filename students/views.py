# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render


# Students views.
def students_list(request):
    import pdb;pdb.set_trace()
    return HttpResponse("<aflkasdhfkjash>")
    # return render(request, 'students/students_list.html', {})


def students_add(request):
    return HttpResponse('<h1> Student Add Form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1> Student %s Editing </h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1> Student %s deleting </h1>' % sid)


# Students views.
def groups_list(request):
    return HttpResponse('<h1> Groups list </h1>')


def groups_add(request):
    return HttpResponse('<h1> Groups Add Form </h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1> Groups %s Editing </h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1> Groups deleting %s</h1>' % gid)
