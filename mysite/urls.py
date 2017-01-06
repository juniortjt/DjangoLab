from django.conf.urls import include, url
from django.contrib import admin
import django.contrib.auth.views
from django.contrib.auth import views
from django.views.generic import CreateView
from photologue.models import Photo, Gallery

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^workshops/', include('photologue.urls', namespace="photologue"), name='workshops'),
    url(r'^workshops/add/$', CreateView.as_view(model=Photo, fields=['title','slug','image'], success_url='/workshops/photo'), name='add-photo'),
    url(r'^accounts/login/$', django.contrib.auth.views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'', include('swiftbook.urls')),
]
