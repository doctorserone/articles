from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    user_o = models.ForeignKey(
        User, related_name="GameUserO", on_delete=models.DO_NOTHING
    )
    # NOTE: The AI opponents will be present in the DB as special users, with its own profile and games
    user_x = models.ForeignKey(
        User, related_name="GameUserX", on_delete=models.DO_NOTHING, null=True
    )
    board = models.CharField(max_length=9)
    creation = models.DateTimeField(auto_now_add=True)
    last_move = models.DateTimeField(auto_now=True)
    winner = models.CharField(max_length=1)


class GameMovement(models.Model):
    user = models.ForeignKey(
        User, related_name="GameMovement", on_delete=models.DO_NOTHING
    )
    game = models.ForeignKey(
        Game, related_name="GameMovement", on_delete=models.DO_NOTHING
    )
    symbol = models.CharField(max_length=1)
    movement = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
