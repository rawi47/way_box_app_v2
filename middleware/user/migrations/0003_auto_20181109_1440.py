# Generated by Django 2.0.8 on 2018-11-09 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20181109_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='bouraoui', max_length=200),
        ),
    ]
