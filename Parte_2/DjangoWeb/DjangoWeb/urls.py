"""
Definition of urls for DjangoWeb.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/',
        LogoutView.as_view(),
        {
            'template_name': 'app/loggedoff.html',
            # 'next_page': '/',
        },
        name='logout'),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
]
