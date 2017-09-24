# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Exam(models.Model):
    """Exam model"""

    class Meta(object):
        verbose_name = u'Іспит'
        verbose_name_plural = u'Іспити'

    subject = models.CharField(max_length=256, blank=False, verbose_name=u'Назва іспиту')
    date_time_exam = models.DateField(blank=False, null=True, verbose_name=u'Дата іспиту')
    teacher = models.CharField(max_length=256, blank=True, verbose_name=u'Прізвище викладача')
    exam_in_group = models.ManyToManyField('Group', blank=False, verbose_name=u'Група')

    def __unicode__(self):
        return u'%s' % self.subject