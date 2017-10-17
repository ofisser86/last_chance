# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.forms import ModelForm, ValidationError
from django.core.urlresolvers import reverse

# Register your models here
from students.models.students import Student
from students.models.groups import Group
from students.models.exams import Exam
from  students.models.monthjournal import MonthJournal


class StudentFormAdmin(ModelForm):
    def clean_student_group(self):
        """Check if student is leader in any group.
            If yes, then ensure it’s the same as selected group."""
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи.', code='invalid')
        return self.cleaned_data['student_group']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['first_name', 'last_name', 'middle_name', 'ticket', 'notes']
    actions = ['copy_students']
    form = StudentFormAdmin

    def copy_students(self, request, queryset):
        for o in queryset:
            o.id = None
            o.save()

    copy_students.short_description = u'Створити копію'

    @staticmethod
    def view_on_site(obj):
        return reverse('students_edit', kwargs={'pk': obj.id})


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    list_display_links = ['title']
    list_editable = ['leader']
    ordering = ['title']
    list_filter = ['leader']
    list_per_page = 10
    search_fields = ['title', 'leader']

    def clean_leader(self):
        pass


admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam)
admin.site.register(MonthJournal)
