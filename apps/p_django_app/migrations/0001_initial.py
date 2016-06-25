# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 22:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poked', models.IntegerField()),
                ('got_poked', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('alias', models.CharField(max_length=45)),
                ('password', models.TextField(max_length=1000)),
                ('email', models.EmailField(max_length=254)),
                ('poked', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            managers=[
                ('userManager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='poking',
            name='who_poked',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='p_django_app.Register'),
        ),
    ]
