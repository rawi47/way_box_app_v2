# Generated by Django 2.2.dev20180916104534 on 2018-10-17 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env_config', '0017_settingapp_cmd_next'),
    ]

    operations = [
        migrations.AddField(
            model_name='settingapp',
            name='command_type',
            field=models.CharField(choices=[('sh', 'Sh'), ('cmd', 'cmd')], default='cmd', max_length=200),
        ),
    ]