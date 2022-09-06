from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    in_game = models.ForeignKey("Match", on_delete=models.SET_NULL, related_name="in_game", null=True)
    elo = models.FloatField(default=0)

class Match(models.Model):

    class Status(models.IntegerChoices):
        WAITING = 0
        ONGOING = 1
        WHITE = 2
        BLACK = 3
        DRAW = 4

    host = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="host", null=True)
    white_player = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="white_player", null=True)
    black_player = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="black_player", null=True)
    fen = models.CharField(max_length=100)
    status = models.IntegerField(choices=Status.choices, default=Status.WAITING)
