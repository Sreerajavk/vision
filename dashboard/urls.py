
from django.contrib import admin
from django.urls import path, include, re_path

from dashboard import views

urlpatterns = [
    path('' , views.dashboard),
    path('add-staff/' , views.add_staff),
    re_path('verify-staff/(?P<token>[0-9a-zA-Z]+)/(?P<email>[0-9a-zA-Z@._]+)/(?P<org_id>[0-9]+)' , views.verify_staff , name='activate')
]
