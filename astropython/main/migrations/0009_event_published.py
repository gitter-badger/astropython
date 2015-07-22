# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20150722_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='published',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
