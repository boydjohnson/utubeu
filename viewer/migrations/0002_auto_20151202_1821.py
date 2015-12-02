# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvitedEmails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_email', models.EmailField(max_length=254)),
                ('loggedin', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='invitedchatroom',
            name='chatroom',
        ),
        migrations.RemoveField(
            model_name='chatroom',
            name='user_emails',
        ),
        migrations.DeleteModel(
            name='InvitedChatroom',
        ),
        migrations.AddField(
            model_name='invitedemails',
            name='chatroom',
            field=models.ForeignKey(related_name='emails_from_chatroom', to='viewer.Chatroom'),
        ),
    ]
