
from django.contrib import admin
from django.urls import path, include, re_path

from dashboard import views

urlpatterns = [
    path('' , views.dashboard),
    path('add-staff/' , views.add_staff),
    path('add-candidates/' ,views.add_candidates ),
    path('upload-images/' , views.upload_images , name = "file_uploads"),
    path('manage/' , views.manage , name = "manage"),
    path('delete-staff/' , views.delete_staff ),
    path('delete-images/' , views.delete_images),
    path('analytics/' , views.analytics),
    re_path('edit-candidate/(?P<id>[0-9]+)' , views.edit_candidate),
    re_path('verify-staff/(?P<token>[0-9a-zA-Z]+)/(?P<email>[0-9a-zA-Z@._]+)/(?P<org_id>[0-9]+)' , views.verify_staff , name='activate')
]
