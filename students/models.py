# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Student(models.Model):
    """Student model"""

    first_name = models.CharField(max_length=256, blank=False, verbose_name=u'Імя')
    last_name = models.CharField(max_length=256, blank=False, verbose_name=u'Прізвище')
    middle_name = models.CharField(max_length=256, blank=True, verbose_name=u'По-бфтькові')
    birthday = models.DateField(blank=False, null=True, verbose_name=u'Дата народження')
    photo = models.ImageField(blank=True, null=True, verbose_name=u'Фото')
    ticket = models.CharField(max_length=256, blank=True, verbose_name=u'Білет')
    notes = models.TextField(blank=True, verbose_name=u'Нотатки')
