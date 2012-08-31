from mock import Mock, patch

from django.test import TestCase
from django.core.urlresolvers import reverse

import models


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
        game_mock = Mock(
            id=1,
            image=Mock(icon=''),
            name='Test',
            platforms=[Mock(id=1)]
        )
        game_mock.name = 'Test'
        giant_mock.return_value = game_mock
        response = self.client.get(reverse('game-detail', args=['1']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Game.objects.count(), 1)

    @patch('giantbomb.giantbomb.Api.getGame')
    def test_game_detail_404(self, giant_mock):
        giant_mock.return_value = None
        response = self.client.get(reverse('game-detail', args=['1']))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(models.Game.objects.count(), 0)
