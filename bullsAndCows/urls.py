from django.conf.urls import patterns, include, url
from bullsAndCows.views import current_datetime, hours_ahead, bulls_cows

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bullsAndCows.views.home', name='home'),
    # url(r'^bullsAndCows/', include('bullsAndCows.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^time/$', current_datetime),
    (r'^time/plus/(\d+)/$', hours_ahead),
    (r'^bulls_cows/$', bulls_cows),
)
