# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms


class ContactForm(forms.Form):
    form_email = forms.EmailField(label=u'Ваша Емейл Адреса')
    subject = forms.CharField(max_length=128, label=u'Заголовок листа')
    message = forms.CharField(max_length=2650, label=u'Текст повідомлення', widget=forms.Textarea)


def contact_admin(request):
    return render(request, 'contact_admin/contact_admin.html', {})

