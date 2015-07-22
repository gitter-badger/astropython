# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20150719_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='published',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='published',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='educationalresource',
            name='published',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='news',
            name='published',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='package',
            name='published',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='snippet',
            name='published',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='published',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='wiki',
            name='published',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
