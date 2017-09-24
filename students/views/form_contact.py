# https://atsoftware.de/2015/02/django-contact-form-full-tutorial-custom-example-in-django-1-7/
# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

from collections import OrderedDict

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


from django.conf import settings
from django import forms
from django.urls import reverse
from django.views.generic import FormView

from contact_form.forms import ContactForm


class ContactFormFields(ContactForm):
    def __init__(self, request, *args, **kwargs):
        # call original initializator
        super(ContactFormFields, self).__init__(request=request, *args, **kwargs)
        fields_keyOrder = ['name', 'email', 'body']
        self.fields = OrderedDict((field_name, self.fields[field_name]) for field_name in fields_keyOrder)
        # this helper object allows us to customize form
        self.helper = FormHelper()

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        # self.helper.form_action = reverse('contact_form')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form buttons
        self.helper.add_input(Submit('send_button', u'Надіслати'))

    recepient_list = [settings.ADMIN_EMAIL]
    email = forms.EmailField(label=u'Ваша Емейл Адреса')
    name = forms.CharField(max_length=128, label=u'Заголовок листа')
    body = forms.CharField(max_length=2650, label=u'Текст повідомлення', widget=forms.Textarea)


class ContactFormView(FormView):
    template_name = 'contact_form/contact_form.html'
    form_class = ContactFormFields
    # success_url = 'contact_form/contact_form_sent.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super(ContactFormView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ContactFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        return reverse('home')
