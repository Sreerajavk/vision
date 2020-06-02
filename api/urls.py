from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
        path('app_login/' , views.login_fn),
        path('get_candidates/',views.get_candidates),
        path('get_user_analytics/' , views.get_analytics),
        path('get_overall_analytics/' , views.overall_analytics),
        path('edit_profile/' , views.edit_profile),
        path('edit_profile_picture/' , views.edit_profile_picture),
        path('add_analytics/' , views.add_analytics),
]
