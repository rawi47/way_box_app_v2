# Generated by Django 2.2.dev20180916104534 on 2018-10-31 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('env_config', '0025_auto_20181031_1052'),
    ]

    operations = [
        migrations.RenameField(
            model_name='settingapp',
            old_name='sup_directory',
            new_name='sub_directory',
        ),
    ]
