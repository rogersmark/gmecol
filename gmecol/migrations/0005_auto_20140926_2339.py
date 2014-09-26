# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gmecol', '0004_auto_20140926_0130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usergame',
            options={'ordering': ('game__name',)},
        ),
    ]
