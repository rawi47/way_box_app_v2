# Generated by Django 2.0.8 on 2018-11-09 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env_config', '0034_env_etc_dir'),
    ]

    operations = [
        migrations.AddField(
            model_name='env',
            name='run_on_start',
            field=models.BooleanField(default=True),
        ),
    ]