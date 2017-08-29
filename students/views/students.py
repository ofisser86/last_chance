# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from ..models.students import Student
from ..models.groups import Group


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

    # paginate students
    paginator = Paginator(students, 5)
    page = request.GET.get('page')

    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results.
        students = paginator.page(paginator.num_pages)

    # import pdb;pdb.set_trace()
    # return HttpResponse("Hello")

    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    groups = Group.objects.all().order_by('title')
    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get('add_button') is not None:
            # TODO: validate input from user
            errors = {}

            if not errors:
                # create student object
                student = Student(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    middle_name=request.POST['middle_name'],
                    birthday=request.POST['birthday'],
                    student_group=Group.objects.get(pk=request.POST['student_group']),
                    photo=request.FILES['photo'],
                )
                student.save()
                # redirect user to students list
                return HttpResponseRedirect(reverse('home'))
            # render form with errors and previous user input
            else:
                return render(request, 'students/students_add.html', {'groups': groups, 'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(reverse('home'))
    else:
        # initial form render
        return render(request, 'students/students_add.html', {'groups': groups})


def students_edit(request, sid):
    return HttpResponse('<h1> Student %s Editing </h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1> Student %s deleting </h1>' % sid)
