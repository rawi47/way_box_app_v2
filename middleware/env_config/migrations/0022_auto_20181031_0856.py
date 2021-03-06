# Generated by Django 2.2.dev20180916104534 on 2018-10-31 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env_config', '0021_installedsoftwares_command'),
    ]

    operations = [
        migrations.AddField(
            model_name='env',
            name='git_repo_update',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='env',
            name='repo_dir',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='env',
            name='repo_dir_update',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='env',
            name='git_repo',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='settingapp',
            name='setting_type',
            field=models.CharField(choices=[('ipset', 'ipset'), ('iptables', 'iptables'), ('dnsmasq', 'dnsmasq'), ('hostapd', 'hostapd'), ('hostapd_conf', 'hostapd config'), ('hosts', 'hosts'), ('interfaces', 'Network interfaces'), ('nodogsplash', 'Nodogsplash')], max_length=200),
        ),
    ]
