# Generated by Django 2.2.dev20180916104534 on 2018-11-02 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env_config', '0029_auto_20181102_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='settingtypes',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]