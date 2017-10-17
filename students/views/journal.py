# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, date
from calendar import monthrange, weekday, day_abbr
from dateutil import relativedelta

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView


from ..models import Student
from ..models import MonthJournal
from ..util import paginate


class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        context = super(JournalView, self).get_context_data(**kwargs)

        # check if we need to display some specific month
        if self.request.GET.get('month'):
            month = datetime.strp_time(self.request.GET['month'], '%Y-%m-%d').date()
        else:
            today = datetime.today()
            month = date(today.year, today.month, 1)

        # calculate current, previous and next month details;
        # we need this for month navigation element in template
        next_month = month + relativedelta(month=1)
        prev_month = month - relativedelta(month=1)
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')

        # we’ll use this variable in students pagination
        context['cur_month'] = month.strftime('%Y-%m-%d')

        # prepare variable for template to generate
        # journal table header elements
        myear, mmonth = month.year, month.month

        number_of_days = monthrange(myear, month)[1]
        # create headers with List Comprehensions
        context['month_header'] = [{'day': d,
                                    'verbose': day_abbr[weekday(myear, month, d)][:2]}
                                   for d in range(1, number_of_days+1)]

        # context['month_header'] = [
        #     {'day': 1, 'verbose': 'Пн'},
        #     {'day': 2, 'verbose': 'Вт'},
        #     {'day': 3, 'verbose': 'Ср'},
        #     {'day': 4, 'verbose': 'Чт'},
        #     {'day': 5, 'verbose': 'Пт'},
        # ]

        # get all students from database
        queryset = Student.objects.order_by('last_name')

        # url to update student presence, for form post
        update_url = reverse('journal')

        # go over all students and collect data about presence
        # during selected month
        students = []

        for student in queryset:
            # try to get journal object by month selected
            # month and current student
            try:
                journal = MonthJournal.objects.all(student=student, date=month)
            except Exception:
                journal = None

            # fill in days presence list for current student
            days = []
            for day in range(1, number_of_days+1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, 'present_day%d' % day, False) or False,
                    'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
                })
            # prepare metadata for current student
            students.append({
                'fullname': u'%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

        context = paginate(students, 10, self.request, context, var_name='students')

        return context
