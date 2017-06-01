# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-29 15:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_manage', '0002_auto_20170529_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchandise',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchandises', to=settings.AUTH_USER_MODEL),
        ),
    ]