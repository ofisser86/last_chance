# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here
from django.core.urlresolvers import reverse

from students.models.students import Student
from students.models.groups import Group
from students.models.exams import Exam


class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['first_name', 'last_name', 'middle_name', 'ticket', 'notes']
    actions = ['copy_students']

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


admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam)
