from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'suggest.views.home', name='home'),
    url(r'^suggest/$', 'suggest.views.suggest', name='suggest'),
    url(r'^entity/$', 'suggest.views.entity', name='entity'),
    url(r'^example/$', 'suggest.views.example', name='entity'),
    url(r'^admin/', include(admin.site.urls)),
)
