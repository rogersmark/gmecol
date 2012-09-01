from mock import Mock, patch

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from gmecol import models


class MockGBResponse(object):

    def __init__(self, id, image, name, platforms, genres):
        self.id = id
        self.image = image
        self.name = name
        self.platforms = platforms
        self.genres = genres


class TestGmeColViews(TestCase):

    def test_index(self):
        ''' Test the index view '''
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    @patch('giantbomb.giantbomb.Api.search')
    def test_search_games(self, giant_mock):
        ''' Test the search for games view '''
        giant_mock.return_value = ''
        response = self.client.get(reverse('search'), {
            'name': 'mario'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(giant_mock.call_args[0][0], 'mario')

    @patch('giantbomb.giantbomb.Api.getGame')
    def test_game_detail(self, giant_mock):
        genre_mock = Mock()
        genre_mock.id = 1
        genre_mock.name = 'test'
        game_mock = MockGBResponse(
            id=1,
            image=Mock(icon=''),
            name='Test',
            platforms=[Mock(id=1)],
            genres=[genre_mock, ]
        )
        giant_mock.return_value = game_mock
        response = self.client.get(reverse('game-detail', args=['1']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['game_root'].remote_id, 1)
        self.assertEqual(response.context['games'].count(), 1)
        assert models.Genre.objects.filter(name='test').exists()

    @patch('giantbomb.giantbomb.Api.getGame')
    def test_game_detail_404(self, giant_mock):
        giant_mock.return_value = None
        response = self.client.get(reverse('game-detail', args=['1']))
        self.assertEqual(response.status_code, 404)

    def test_game_platform_detail(self):
        response = self.client.get(reverse('game-platform-detail',
            args=[8015, 122]
        ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['game'].name, 'Quake')

    def test_add_game_to_collection(self):
        assert self.client.login(username='test_user', password='test')
        response = self.client.get(reverse('add-game-to-collection',
            args=[8015, 122]
        ))
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='test_user')
        quake = models.Game.objects.get(name='Quake')
        assert quake in user.userprofile.games.all()
