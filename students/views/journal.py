# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from calendar import monthrange, weekday, day_abbr
from dateutil import relativedelta

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView


from students.models import Student
from ..models import MonthJournal
from ..util import paginate


class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        context = super(JournalView, self).get_context_data(**kwargs)

        today = datetime.today()
        month = datetime.date(today.year, today.month)

        context['prev_month'] = '2017-09-17'
        context['next_month'] = '2017-11-17'
        context['year'] = '2017'
        context['cur_month'] = '2017-10-17'

        context['month_header'] = [
            {'day': 1, 'verbose': 'Пн'},
            {'day': 2, 'verbose': 'Вт'},
            {'day': 3, 'verbose': 'Ср'},
            {'day': 4, 'verbose': 'Чт'},
            {'day': 5, 'verbose': 'Пт'},
        ]

        queryset = Student.objects.order_by('last_name')


        update_url = reverse('journal')

        students = []

        for student in queryset:
            days = []

            for day in range(1, 31):
                days.append({
                    'day':day,
                    'present': True,
                    'date': datetime.date(2017, 10, day).strftime('%Y-%m-%d'),
                })
            students.append({
                'fullname': u'%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

        context = paginate(students, 10, self.request. context, var_name='students')

        return context