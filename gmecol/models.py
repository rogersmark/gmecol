from django.db import models


class BaseModel(models.Model):
    ''' Abstract base model providing standard fields that most models in this
    project will require.
    '''

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Platform(BaseModel):
    ''' Houses the various platforms that games are playable on, i.e. Xbox,
    PS3, etc.
    '''

    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)


class Game(BaseModel):
    ''' Table for holding game entries '''

    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    platform = models.ForeignKey('Platform')


class UserGame(BaseModel):
    ''' Through model for games owned by a user. Provides extra information
    for that M2M relationship such as game ratings.
    '''

    RATINGS = [(x, x) for x in range(0, 6)]

    game = models.ForeignKey('Game')
    user = models.ForeignKey('UserProfile')
    rating = models.IntegerField(choices=RATINGS, default=3)
    for_trade = models.BooleanField(default=False)
    for_sale = models.BooleanField(default=False)

class UserProfile(BaseModel):
    ''' Profile for tracking a user's information and catalog '''

    user = models.OneToOneField('auth.User')
    games = models.ManyToManyField('Game', through='UserGame')
    platforms = models.ManyToManyField('Platform')
