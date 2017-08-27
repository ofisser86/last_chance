# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here
from students.models.students import Student
from students.models.groups import Group
from students.models.exams import Exam

admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Exam)
