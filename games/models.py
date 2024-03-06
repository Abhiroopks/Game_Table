import json
from django.db import models

class MLBGame(models.Model):
    id = models.BigAutoField(primary_key=True)
    datetime = models.DateTimeField()
    home_team = models.TextField()
    away_team = models.TextField()
    location = models.TextField()
    # home_team_ranking = models.SmallIntegerField()
    # away_team_ranking = models.SmallIntegerField()
    
    def to_dict(self):
        """
        Serializes this object to a json string.
        """
        
        return {
            "date": self.datetime.strftime("%Y-%m-%d"),
            "time": self.datetime.strftime("%I:%M %p %Z"),
            "home_team": self.home_team,
            "away_team": self.away_team,
            "location": self.location
        }
    
        

