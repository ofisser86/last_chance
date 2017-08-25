# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

from ..models import Student


# Students views.
def students_list(request):
    students = Student.objects.all().order_by('last_name')

    # try to order students list
    order_by = request.GET.get('order_by', '')

    # order_by for students count
    if order_by == 'count':
        students = students.order_by('id')
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # import pdb;pdb.set_trace()
    # return HttpResponse("Hello")

    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    return HttpResponse('<h1> Student Add Form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1> Student %s Editing </h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1> Student %s deleting </h1>' % sid)