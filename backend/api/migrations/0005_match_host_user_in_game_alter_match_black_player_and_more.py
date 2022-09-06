# Generated by Django 4.1 on 2022-09-06 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_match_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='host', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='in_game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='in_game', to='api.match'),
        ),
        migrations.AlterField(
            model_name='match',
            name='black_player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='black_player', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='match',
            name='status',
            field=models.IntegerField(choices=[(0, 'Waiting'), (1, 'Ongoing'), (2, 'White'), (3, 'Black'), (4, 'Draw')], default=0),
        ),
        migrations.AlterField(
            model_name='match',
            name='white_player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='white_player', to=settings.AUTH_USER_MODEL),
        ),
    ]
