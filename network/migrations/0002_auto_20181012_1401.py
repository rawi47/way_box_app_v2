# Generated by Django 2.2.dev20180916104534 on 2018-10-12 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='networks',
            name='af_inet6_addr',
        ),
        migrations.RemoveField(
            model_name='networks',
            name='af_inet6_broadcast',
        ),
        migrations.RemoveField(
            model_name='networks',
            name='af_inet6_netmask',
        ),
        migrations.RemoveField(
            model_name='networks',
            name='af_inet6_peer',
        ),
        migrations.RemoveField(
            model_name='networks',
            name='af_inet_addr',
        ),
        migrations.RemoveField(
            model_name='networks',
            name='af_inet_broadcast',
        ),
        migrations.RemoveField(
            model_name='networks',
            name='af_inet_netmask',
        ),
        migrations.RemoveField(
            model_name='networks',
            name='af_inet_peer',
        ),
        migrations.RemoveField(
            model_name='networks',
            name='af_link_addr',
        ),
        migrations.RemoveField(
            model_name='networks',
            name='af_link_broadcast',
        ),
        migrations.RemoveField(
            model_name='networks',
            name='af_link_netmask',
        ),
        migrations.RemoveField(
            model_name='networks',
            name='af_link_peer',
        ),
        migrations.CreateModel(
            name='AfLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('af_link_addr', models.CharField(default='', max_length=200)),
                ('af_link_broadcast', models.CharField(default='', max_length=200)),
                ('af_link_netmask', models.CharField(default='', max_length=200)),
                ('af_link_peer', models.CharField(default='', max_length=200)),
                ('networks_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.Networks')),
            ],
        ),
    ]