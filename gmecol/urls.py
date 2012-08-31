from django.conf.urls.defaults import *

urlpatterns = patterns('gmecol.views',
    url('^search/$', 'search', name='search'),
)
