# Generated by Django 2.2.dev20180916104534 on 2018-10-12 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Networks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='name', max_length=200)),
                ('af_link_addr', models.CharField(default='', max_length=200)),
                ('af_link_broadcast', models.CharField(default='', max_length=200)),
                ('af_link_netmask', models.CharField(default='', max_length=200)),
                ('af_link_peer', models.CharField(default='', max_length=200)),
                ('af_inet_addr', models.CharField(default='', max_length=200)),
                ('af_inet_broadcast', models.CharField(default='', max_length=200)),
                ('af_inet_netmask', models.CharField(default='', max_length=200)),
                ('af_inet_peer', models.CharField(default='', max_length=200)),
                ('af_inet6_addr', models.CharField(default='', max_length=200)),
                ('af_inet6_broadcast', models.CharField(default='', max_length=200)),
                ('af_inet6_netmask', models.CharField(default='', max_length=200)),
                ('af_inet6_peer', models.CharField(default='', max_length=200)),
            ],
        ),
    ]
