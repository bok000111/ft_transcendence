from django.db import models

# Create your models here.
class PongMatchData (models.Model):
    player1 = models.CharField(max_length=100)
    player2 = models.CharField(max_length=100)
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    winner = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.player1 + " vs " + self.player2 + " " + str(self.score1) + " : " + str(self.score2) + " " + self.winner + " " + str(self.date)