"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from students.views import students, groups, journal, exams, demo, contact_admin, profile, form_contact
from settings import MEDIA_ROOT, DEBUG

urlpatterns = [
                  # Students urls
                  url(r'^$', students.students_list, name='home'),
                  url(r'^students/add/$', students.students_add, name='students_add'),
                  url(r'^students/(?P<pk>\d+)/edit/$', students.StudentUpdateView.as_view(), name='students_edit'),
                  url(r'^students/(?P<pk>\d+)/delete/$', students.StudentDeleteView.as_view(), name='students_delete'),
                  url(r'^students/(?P<sid>\d+)/profile/$', profile.students_profile, name='profile'),

                  # Groups urls
                  url(r'^groups/$', groups.groups_list, name='groups_list'),
                  url(r'^groups/add$', groups.groups_add, name='groups_add'),
                  url(r'^groups/(?P<gid>\d+)/edit/$', groups.groups_edit, name='groups_edit'),
                  url(r'^groups/(?P<gid>\d+)/delete/$', groups.groups_delete, name='groups_delete'),

                  # Journal urls
                  url(r'^journal/(?P<pk>\d+)?/?$', journal.JournalView.as_view(), name='journal'),

                  # Journal urls
                  url(r'^exams/$', exams.exams_list, name='exams_list'),
                  url(r'^exams/add/$', exams.exams_add, name='exams_add'),
                  url(r'^exams/(?P<eid>\d+)/edit/$', exams.exams_edit, name='exams_edit'),
                  url(r'^exams/(?P<eid>\d+)/delete/$', exams.exams_delete, name='exams_delete'),

                  # Demo urls
                  url(r'^demo/$', demo.demo, name='demo'),

                  # Contact admin url
                  url(r'^contact-admin/$', contact_admin.contact_admin, name='contact_admin'),
                  # Contact admin url use CBV and django-contact-form
                  # url(r'^contact/', include('contact_form.urls')),
                  url(r'^contact/', form_contact.ContactFormView.as_view(), name='contact_form'),
                  url(r'^contact/sent/',
                      form_contact.ContactFormView.as_view(),
                      name='contact_form_sent'),

                  # Admin url
                  url(r'^admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
