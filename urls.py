from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.decorators.csrf import csrf_exempt

from example.views import Index, NewBuild, PushBuild

urlpatterns = patterns('example.views',
    url(r'^/?$', Index.as_view(), name='index'),
    url(r'^ajax/build/new', csrf_exempt(NewBuild.as_view()), name='ajax_new_build'),
    url(r'^push/build/(?P<id>\d+)', csrf_exempt(PushBuild.as_view()), name='push_get_build_info'),
)

urlpatterns += staticfiles_urlpatterns()
