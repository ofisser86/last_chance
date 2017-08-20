# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render


# Students views.
def students_list(request):
    students = (
        {'id': 1,
         'first_name': 'Марта',
         'last_name': 'Адамчук',
         'ticket': 21,
         'img': 'img/marta.jpeg',
         },
        {'id': 2,
         'first_name': 'Світлана',
         'last_name': 'Сікора',
         'ticket': 31,
         'img': 'img/sikora.jpeg',
         },
    )

    # import pdb;pdb.set_trace()
    # return HttpResponse("Hello")

    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    return HttpResponse('<h1> Student Add Form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1> Student %s Editing </h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1> Student %s deleting </h1>' % sid)