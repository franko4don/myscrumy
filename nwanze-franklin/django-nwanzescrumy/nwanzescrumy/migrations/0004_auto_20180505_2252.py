# Generated by Django 2.0.5 on 2018-05-05 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nwanzescrumy', '0003_auto_20180505_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]