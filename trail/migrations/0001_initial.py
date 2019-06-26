# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-04 08:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_identity', models.UUIDField()),
                ('version_id', models.UUIDField(unique=True)),
                ('version_state', models.PositiveSmallIntegerField(choices=[(0, 'Invalid'), (100, 'Draft'), (200, 'Published'), (300, 'Archived')], default=0)),
                ('version_created_at', models.DateTimeField(auto_now_add=True)),
                ('version_last_updated_at', models.DateTimeField(auto_now_add=True)),
                ('version_description', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='recorder',
            unique_together=set([('version_identity', 'version_id')]),
        ),
    ]