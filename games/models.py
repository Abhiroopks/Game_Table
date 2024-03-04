from django.db import models

class MLBGame(models.Model):
    id = models.BigAutoField(primary_key=True)
    datetime = models.DateTimeField()
    home_team = models.TextField()
    away_team = models.TextField()
    location = models.TextField()
    # home_team_ranking = models.SmallIntegerField()
    # away_team_ranking = models.SmallIntegerField()

