# Generated by Django 4.1 on 2022-09-15 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='black_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='white_points',
            field=models.IntegerField(default=0),
        ),
    ]
