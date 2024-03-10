import json

from django.db import models


class MLBGame(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    game_type = models.TextField()
    home_team = models.TextField()
    away_team = models.TextField()
    home_win_pct = models.FloatField()
    away_win_pct = models.FloatField()
    win_pct_prod = models.FloatField()
    location = models.TextField()

    def to_dict(self):
        """
        Serializes this object to a json string.
        """

        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "game_type": self.game_type,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "home_win_pct": self.home_win_pct,
            "away_win_pct": self.away_win_pct,
            "win_pct_prod": self.win_pct_prod,
            "location": self.location,
        }
