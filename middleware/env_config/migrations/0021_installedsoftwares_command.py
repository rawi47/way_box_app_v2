# Generated by Django 2.2.dev20180916104534 on 2018-10-22 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env_config', '0020_settingapp_command_type_next'),
    ]

    operations = [
        migrations.AddField(
            model_name='installedsoftwares',
            name='command',
            field=models.CharField(default='', max_length=200),
        ),
    ]