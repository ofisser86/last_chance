# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from ..models.exams import Exam


# Exams views.

def exams_list(request):
    exams = Exam.objects.all()
    for i in exams:
        print(i)
    return render(request, 'students/exams.html', {'exams': exams})


def exams_add(request):
    return HttpResponse('<h1> Exam Add Form</h1>')


def exams_edit(request, eid):
    return HttpResponse('<h1> Exam %s Editing </h1>' % eid)


def exams_delete(request, eid):
    return HttpResponse('<h1> Exam %s deleting </h1>' % eid)