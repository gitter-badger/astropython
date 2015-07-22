# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_event_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='category',
            field=models.CharField(max_length=60),
        ),
    ]
