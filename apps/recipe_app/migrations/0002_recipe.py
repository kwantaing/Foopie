# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-27 18:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_id', models.IntegerField()),
                ('title', models.CharField(max_length=225)),
                ('instructions', models.TextField()),
                ('image', models.URLField()),
                ('favoritedby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipe_app.User')),
            ],
        ),
    ]
