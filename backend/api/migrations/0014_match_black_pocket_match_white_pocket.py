# Generated by Django 4.1 on 2022-09-18 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_match_black_points_match_white_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='black_pocket',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='match',
            name='white_pocket',
            field=models.JSONField(default=dict),
        ),
    ]
