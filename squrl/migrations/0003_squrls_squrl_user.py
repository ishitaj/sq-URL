# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-20 17:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('squrl', '0002_auto_20170814_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='squrls',
            name='squrl_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
