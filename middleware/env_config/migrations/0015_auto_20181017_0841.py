# Generated by Django 2.2.dev20180916104534 on 2018-10-17 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env_config', '0014_auto_20181016_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='settingapp',
            name='cmd',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='env',
            name='api_mode',
            field=models.CharField(choices=[('commun', 'commun'), ('wlan', 'wlan'), ('eth', 'eth')], max_length=200),
        ),
        migrations.AlterField(
            model_name='settingapp',
            name='api_mode',
            field=models.CharField(choices=[('commun', 'commun'), ('wlan', 'wlan'), ('eth', 'eth')], max_length=200),
        ),
    ]
