# Generated by Django 2.2.dev20180916104534 on 2018-10-03 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env_config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='env',
            name='git_repo',
            field=models.CharField(max_length=200),
        ),
    ]
