from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views.games import GameListView

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
    url('^collection/game/(?P<game_id>\d+)/add/$',
        'add_game_to_collection', name='add-game-to-collection'),
    url('^collection/$', GameListView.as_view(wish=False), name='view-collection'),
    url('^collection/rate/(?P<game_id>\d+)/$',
        'rate_game', name='rate-game'),
    url('^collection/trade/(?P<game_id>\d+)/$',
        'toggle_trade_and_sale', name='trade-game'),
    url('^collection/sell/(?P<game_id>\d+)/$',
        'toggle_trade_and_sale', {'trade': False}, name='sell-game'),
)

# game wishlist
urlpatterns += patterns('gmecol.views.collection',
    url('^wish/game/(?P<game_id>\d+)/add/$',
        'add_game_to_collection', {'wish': True}, name='add-game-to-wish'),
    url('^wishlist/$', GameListView.as_view(wish=True), name='wishlist'),
)

# profile
urlpatterns += patterns('gmecol.views.profile',
    url('^profile/(?P<user_id>\d+)/$', 'profile', name='profile'),
    url(r'^profile/update-email/$', 'update_email', name='update-email'),
)

urlpatterns += patterns('',
    url(
        '^profile/password-change/$',
        'django.contrib.auth.views.password_change',
        {
            'template_name': 'accounts/password_change.html',
            'post_change_redirect': 'password-change-done'
        },
        name='password-change'
    ),
    url(
        '^profile/password-changed/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'accounts/password_change_done.html'},
        name='password-change-done'
    ),
)

# friends
urlpatterns += patterns('gmecol.views.manage_friends',
    url('^friend/list/$', 'list_friends', name='list-friends'),
    url('^friend/add/(?P<friend_pk>\d+)/$',
        'add_friend', name='add-friend'),
    url('^friend/remove/(?P<friend_pk>\d+)/$',
        'remove_friend', name='remove-friend'),
)

# messaging views
urlpatterns += patterns('gmecol.views.messages',
    url('^messages/$', 'message_list', name='message-list'),
    url('^messages/send/$', 'send_message', name='send-message'),
    url('^messages/(?P<message_id>\d+)/$',
        'message_detail', name='message-detail'),
)

# other
urlpatterns += patterns('',
    url(
        r'^about/$',
        TemplateView.as_view(template_name="gmecol/about.html"),
        name='about'
    )
)
