# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gmecol', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='image_url',
        ),
        migrations.AddField(
            model_name='game',
            name='deck',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='icon_image_url',
            field=models.CharField(default='', max_length=b'256', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='med_image_url',
            field=models.CharField(default='', max_length=b'256', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='screen_image_url',
            field=models.CharField(default='', max_length=b'256', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='sm_image_url',
            field=models.CharField(default='', max_length=b'256', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='super_image_url',
            field=models.CharField(default='', max_length=b'256', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='thumb_image_url',
            field=models.CharField(default='', max_length=b'256', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='tiny_image_url',
            field=models.CharField(default='', max_length=b'256', blank=True),
            preserve_default=False,
        ),
    ]
