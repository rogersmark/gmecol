from django.conf.urls.defaults import *

urlpatterns = patterns('gmecol.views',
    url('^$', 'index', name='index'),
    url('^game/(?P<remote_id>\d+)/$', 'game_detail', name='game-detail'),
    url('^search/$', 'search', name='search'),
)
