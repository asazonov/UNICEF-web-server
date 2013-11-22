from django.conf.urls import patterns, include, url

from django.contrib import admin

import GeoServer
import UNICEFServer

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'UNICEFServer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^send/$', GeoServer.views.send),
    url(r'^receive/$', GeoServer.views.receive),
    url(r'^check/$', GeoServer.views.check),
    url(r'^$', UNICEFServer.views.index),
    url(r'^get_messages/$', GeoServer.views.getMessages),
    url(r'^get_users/$', GeoServer.views.getUsers),
    )
