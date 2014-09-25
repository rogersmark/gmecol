# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('gmecol', '0002_auto_20140923_0328'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='release_date',
            field=models.DateField(default=datetime.date(2014, 9, 23)),
            preserve_default=False,
        ),
    ]
