# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chatroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(max_length=50, verbose_name='Chatroom Name')),
                ('description', models.TextField(null=True, max_length=100, blank=True)),
                ('owner', models.ForeignKey(related_name='owned_chatrooms', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='joined_chatrooms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvitedEmails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_email', models.EmailField(max_length=254)),
                ('loggedin', models.BooleanField(default=False)),
                ('chatroom', models.ForeignKey(related_name='invited_emails', to='viewer.Chatroom')),
            ],
        ),
    ]
