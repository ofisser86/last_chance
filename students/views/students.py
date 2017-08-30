# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

from datetime import datetime

from PIL import Image

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
            # errors collection
            errors = {}
            data = {'middle_name': request.POST.get('middle_name', ''), 'notes': request.POST.get('notes', '')}

            # validate user input
            first_name = request.POST.get('first_name', '').strip()

            if not first_name:
                errors['first_name'] = u'Імя є обовязковим'
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()

            if not last_name:
                errors['last_name'] = u'Прізвище є обовязковим'
            else:
                data['last_name'] = last_name

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u'Білет є обовязковим'
            else:
                data['ticket'] = ticket

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u'Дата народження є обовязковою'
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u'Введіть коректний формат дати'

                else:
                    data['birthday'] = birthday

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u'Оберіть групу для студента'
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u'Оберіть коректну групу'
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            valid_image_extention = [
                "JPEG",
                "JPG",
                "PNG",
                "GIF",
            ]

            try:
                photo_format = Image.open(photo)
            except Exception:
                errors['photo'] = u'Завантажте коректне фото'
            else:
                if photo_format.format not in valid_image_extention:
                    errors['photo'] = u'Невірний формат файлу'
                elif photo.size > 2 * 1024 * 1024:
                    errors['photo'] = u'Фото не більше 2мб'
                else:
                    data['photo'] = photo

            # save student
            if not errors:
                student = Student(**data)
                student.save()

                # redirect to students list
                return HttpResponseRedirect(u'%s?status_message=Студента %s %s успішно додано!' % (
                    reverse('home'), student.first_name, student.last_name))
            else:
                # render form with errors and previous user input
                messages.error(request, u'Будь-ласка, виправте наступні помилки')
                return render(request, 'students/students_add.html', {'groups': groups, 'errors': errors})

                # if not errors:
                #     # create student object
                #     student = Student(
                #         first_name=request.POST['first_name'],
                #         last_name=request.POST['last_name'],
                #         middle_name=request.POST['middle_name'],
                #         birthday=request.POST['birthday'],
                #         ticket=request.POST['ticket'],
                #         student_group=Group.objects.get(pk=request.POST['student_group']),
                #         photo=request.FILES['photo'],
                #     )
                #     student.save()
                #     # redirect user to students list
                #     return HttpResponseRedirect(reverse('home'))
                # # render form with errors and previous user input
                # else:
                #     return render(request, 'students/students_add.html', {'groups': groups, 'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(u'%s?status_message=Додавання студетна скасовано!' % reverse('home'))
    else:
        # initial form render
        return render(request, 'students/students_add.html', {'groups': groups})


def students_edit(request, sid):
    return HttpResponse('<h1> Student %s Editing </h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1> Student %s deleting </h1>' % sid)
