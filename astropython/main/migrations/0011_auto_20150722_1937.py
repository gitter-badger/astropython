# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20150722_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.RemoveField(
            model_name='package',
            name='category',
        ),
        migrations.AddField(
            model_name='package',
            name='category',
            field=models.ManyToManyField(to='main.PackageCategory'),
        ),
    ]
