# Generated by Django 4.1 on 2022-09-02 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='elo',
            field=models.FloatField(default=0),
        ),
    ]
