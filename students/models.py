# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Student(models.Model):
    """Student model"""

    class Meta(object):
        verbose_name = u'Студент'
        verbose_name_plural = u'Студенти'

    first_name = models.CharField(max_length=256, blank=False, verbose_name=u'Імя')
    last_name = models.CharField(max_length=256, blank=False, verbose_name=u'Прізвище')
    middle_name = models.CharField(max_length=256, blank=True, verbose_name=u'По-батькові')
    birthday = models.DateField(blank=False, null=True, verbose_name=u'Дата народження')
    photo = models.ImageField(blank=True, null=True, verbose_name=u'Фото')
    ticket = models.CharField(max_length=256, blank=True, verbose_name=u'Білет')
    notes = models.TextField(blank=True, verbose_name=u'Нотатки')

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Group(models.Model):
    """Group model"""

    class Meta(object):
        verbose_name = u'Група'
        verbose_name_plural = u'Групи'

    title = models.CharField(max_length=256, blank=False, verbose_name=u'Назва')
    leader = models.OneToOneField('Student', blank=True, null=True, on_delete=models.SET_NULL, verbose_name=u'Староста')
    notes = models.TextField(blank=True, verbose_name=u'Нотатки')

    def __unicode__(self):
        if self.leader:
            return u'%s (%s %s)' % (self.title, self.leader.first_name, self.leader.last_name)
        else:
            return u'%s' % self.title