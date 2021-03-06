# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
from django.forms import ModelForm

from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from PIL import Image


from ..models.students import Student
from ..models.groups import Group
from ..util import paginate, get_current_group


class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes

        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.layout[-1] = FormActions(
            Submit('add_button', u'Зберегти', css_class='btn btn-primary'),
            Submit('cancel_button', u'Скасувати', css_class='btn btn-link')
        )


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm
    # fields = '__all__'

    def get_success_url(self):
        return u'%s?status_message=Студента успішно збережено!' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Редагування студента відмінено!' % reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message=Студента успішно видалено!' % reverse('home')


# Students views.
def students_list(request):
    # check if we need to show only one group of students
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
        # otherwise show all students
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
    # paginator = Paginator(students, 5)
    # page = request.GET.get('page')
    #
    # try:
    #     students = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer, deliver first page.
    #     students = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range (e.g. 9999), deliver
    #     # last page of results.
    #     students = paginator.page(paginator.num_pages)

    # import pdb;pdb.set_trace()
    # return HttpResponse("Hello")

    context = paginate(students, 5, request, {}, var_name='students')

    return render(request, 'students/students_list.html', context)


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
