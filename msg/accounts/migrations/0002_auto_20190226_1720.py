# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-02-26 17:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='date_joines',
            new_name='date_joined',
        ),
    ]
