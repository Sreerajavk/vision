from django.contrib import admin
from django.urls import path, include

from api import views

urlpatterns = [
        path('app_login/' , views.login_fn),
        path('get_candidates/',views.get_candidates),
        path('get_user_analytics/' , views.get_analytics)
]
