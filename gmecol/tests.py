from mock import Mock, patch

from django.test import TestCase
from django.core.urlresolvers import reverse


class MockGBResponse(object):

    def __init__(self, id, image, name, platforms):
        self.id = id
        self.image = image
        self.name = name
        self.platforms = platforms


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
        game_mock = MockGBResponse(
            id=1,
            image=Mock(icon=''),
            name='Test',
            platforms=[Mock(id=1)]
        )
        giant_mock.return_value = game_mock
        response = self.client.get(reverse('game-detail', args=['1']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['game_root'].remote_id, 1)
        self.assertEqual(response.context['games'].count(), 1)

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
