"""vision URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.conf.urls import handler404, handler500

from dashboard import views
from vision import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('api/', include('api.urls')),
    path('', views.index),
    path('org-signup/', views.org_signup),
    path('add-organisation/', views.add_organisation),
    path('login/', views.login_fn),
    path('staff-signup/', views.staff_signup),
    path('logout/' , views.logout_fn),
    # re_path('.*', views.error_page)
]

# handler404 = 'dashboard.views.error_page'


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns.append(re_path('.*', views.error_page))
# urlpatterns +=
# print(urlpatterns)
