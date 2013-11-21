from django.conf.urls import patterns, include, url

from django.contrib import admin

import GeoServer

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'UNICEFServer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^send/$', GeoServer.views.send),
    url(r'^receive/$', GeoServer.views.receive),  # Pass a text message to the processing server
    url(r'^check/$', GeoServer.views.check),



)
