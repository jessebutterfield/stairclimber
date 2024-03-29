from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stairclimber.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^month/(\d+)/(\d+)/(prev|next)$', 'countstairs.views.newMonth'),
    url(r'^month/(\d+)/(\d+)/$', 'countstairs.views.month'),
    url(r'^month/$', 'countstairs.views.currentMonth'),
    url(r'^oneTime/', 'countstairs.views.oneTimeAdd'),
    url(r'^addPreset/(?P<id>\d+)', 'countstairs.views.addPreset'),
    url(r'^newPreset/(?P<id>\d+)', 'countstairs.views.newPreset'),
    url(r'^editPreset/', 'countstairs.views.editCustomSettings'),
    url(r'^$', 'countstairs.views.home'),
)
