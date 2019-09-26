# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-28 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_app', '0005_auto_20190627_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='myRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('instructions', models.TextField()),
                ('image', models.URLField()),
                ('readyInMinutes', models.IntegerField()),
                ('ingredients', models.TextField()),
                ('createdby', models.ManyToManyField(related_name='myrecipes', to='recipe_app.User')),
            ],
        ),
    ]