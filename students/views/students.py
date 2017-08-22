# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

from studentsdb.settings import BASE_DIR
from ..models import Student


# Students views.
def students_list(request):
    students = Student.objects.all()
    # import pdb;pdb.set_trace()
    # return HttpResponse("Hello")

    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    return HttpResponse('<h1> Student Add Form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1> Student %s Editing </h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1> Student %s deleting </h1>' % sid)