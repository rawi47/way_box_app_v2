# Generated by Django 2.1.2 on 2018-11-09 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env_config', '0037_env_branche'),
    ]

    operations = [
        migrations.AlterField(
            model_name='env',
            name='root_dir',
            field=models.CharField(default='/home/pi', max_length=200),
        ),
    ]
