# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-15 16:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insta_clone', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='profile',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='insta_clone.Profile'),
        ),
    ]
