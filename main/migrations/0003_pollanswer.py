# Generated by Django 5.0.6 on 2024-06-09 19:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_poll_poll_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poll', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.poll')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.user')),
            ],
        ),
    ]