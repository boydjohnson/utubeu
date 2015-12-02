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
                ('name', models.TextField(max_length=50, verbose_name=b'Chatroom Name')),
                ('description', models.TextField(max_length=100, null=True, blank=True)),
                ('owner', models.ForeignKey(related_name='chatroom_from_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvitedChatroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_email', models.EmailField(max_length=254)),
                ('number_in', models.IntegerField(default=0)),
                ('loggedin', models.BooleanField(default=False)),
                ('chatroom', models.OneToOneField(related_name='invited_room', to='viewer.Chatroom')),
            ],
        ),
        migrations.AddField(
            model_name='chatroom',
            name='user_emails',
            field=models.ManyToManyField(related_name='chatroom_from_emails', to='viewer.InvitedChatroom'),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='users',
            field=models.ManyToManyField(related_name='chatroom_from_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
