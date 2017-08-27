# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Exam(models.Model):
    """Group model"""

    class Meta(object):
        verbose_name = u'Іспит'
        verbose_name_plural = u'Іспити'

    title = models.CharField(max_length=256, blank=False, verbose_name=u'Назва')
    leader = models.OneToOneField('Student', blank=True, null=True, on_delete=models.SET_NULL, verbose_name=u'Староста')
    notes = models.TextField(blank=True, verbose_name=u'Нотатки')

    def __unicode__(self):
        if self.leader:
            return u'%s (%s %s)' % (self.title, self.leader.first_name, self.leader.last_name)
        else:
            return u'%s' % self.title