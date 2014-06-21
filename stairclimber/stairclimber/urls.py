from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stairclimber.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^oneTime/', 'countstairs.views.oneTimeAdd'),
    url(r'^addPreset/(?P<id>\d+)', 'countstairs.views.addPreset'),
    url(r'^$', 'countstairs.views.home'),
)
