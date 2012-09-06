from django.conf.urls.defaults import *

# general
urlpatterns = patterns('gmecol.views.main',
    url('^$', 'index', name='index'),
    url('^game/(?P<remote_id>\d+)/$', 'game_detail', name='game-detail'),
    url('^game/(?P<game_id>\d+)/platform/(?P<platform_id>\d+)/$',
        'game_platform_detail', name='game-platform-detail'),
    url('^search/$', 'search', name='search'),
)

# game collection
urlpatterns += patterns('gmecol.views.collection',
    url('^game/(?P<game_id>\d+)/platform/(?P<platform_id>\d+)/add/$',
        'add_game_to_collection', name='add-game-to-collection'),
    url('^collection/$', 'view_collection', name='view-collection'),
    url('^collection/genre/(?P<genre_id>\d+)/$',
        'view_collection_by_genre', name='collection-by-genre'),
    url('^collection/platform/(?P<platform_id>\d+)/$',
        'view_collection_by_platform', name='collection-by-platform'),
    url('^collection/rate/(?P<game_id>\d+)/$',
        'rate_game', name='rate-game'),
)

# profile
urlpatterns += patterns('gmecol.views.profile',
    url('^profile/(?P<user_id>\d+)/$', 'profile', name='profile'),
)

# messaging views
urlpatterns += patterns('gmecol.views.messages',
    url('^messages/$', 'message_list', name='message_list'),
    url('^messages/send/$', 'send_message', name='send-message'),
    url('^messages/(?P<message_id>\d+)/$',
        'message_detail', name='message-detail'),
)
