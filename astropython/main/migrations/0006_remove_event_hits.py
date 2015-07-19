# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150719_1934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='hits',
        ),
    ]
