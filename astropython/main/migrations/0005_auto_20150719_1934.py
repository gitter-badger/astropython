# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_feed_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='announcement',
            name='hits',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='hits',
        ),
        migrations.RemoveField(
            model_name='educationalresource',
            name='hits',
        ),
        migrations.RemoveField(
            model_name='news',
            name='hits',
        ),
        migrations.RemoveField(
            model_name='package',
            name='hits',
        ),
        migrations.RemoveField(
            model_name='snippet',
            name='hits',
        ),
        migrations.RemoveField(
            model_name='tutorial',
            name='hits',
        ),
        migrations.RemoveField(
            model_name='wiki',
            name='hits',
        ),
        migrations.AlterField(
            model_name='announcement',
            name='abstract',
            field=models.TextField(default=b'', help_text=b'Optional Summary of Post', blank=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='abstract',
            field=models.TextField(default=b'', help_text=b'Optional Summary of Post', blank=True),
        ),
        migrations.AlterField(
            model_name='educationalresource',
            name='abstract',
            field=models.TextField(default=b'', help_text=b'Optional Summary of Post', blank=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='abstract',
            field=models.TextField(default=b'', help_text=b'Optional Summary of Post', blank=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='abstract',
            field=models.TextField(default=b'', help_text=b'Optional Summary of Post', blank=True),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='abstract',
            field=models.TextField(default=b'', help_text=b'Optional Summary of Post', blank=True),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='abstract',
            field=models.TextField(default=b'', help_text=b'Optional Summary of Post', blank=True),
        ),
        migrations.AlterField(
            model_name='wiki',
            name='abstract',
            field=models.TextField(default=b'', help_text=b'Optional Summary of Post', blank=True),
        ),
    ]
