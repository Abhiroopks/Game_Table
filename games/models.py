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
    home_league_rank = models.IntegerField()
    away_league_rank = models.IntegerField()
    home_div = models.TextField()
    away_div = models.TextField()
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
            "home_league_rank": self.home_league_rank,
            "away_league_rank": self.away_league_rank,
            "home_div": self.home_div,
            "away_div": self.away_div,
            "location": self.location,
        }
