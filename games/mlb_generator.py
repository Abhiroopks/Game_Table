from datetime import date, timedelta

import statsapi as mlb_api

from games.models import MLBGame


class Location():
    """
    Container for storing basic location data
    """
    def __init__(self, city, state, country):
        self.city = city
        self.state = state
        self.country = country
    
    def get_query(self):
        """
        Returns string query of this location
        """
        return f"{self.city}, {self.state}, {self.country}"

class MLBGenerator():
    """
    Class for managing the retrieval of MLB games and associated game data.
    """
    def update_table_data(self, days: int):
        """
        Queries schedule and weather api to generate table data.
        
        :arg days: Number of days to look ahead when fetching games.
        :returns: None
        """
        games = self.__get_games(days)
        for game in games:
            game_record: MLBGame = MLBGame()
            game_record.id = game["game_id"]
            game_record.datetime = game["game_datetime"]
            game_record.home_team = game["home_name"]
            game_record.away_team = game["away_name"]
            
            location: Location = self.__get_location(game)
            game_record.location = location.get_query()
            
            game_record.save()
            
            
        
        
    
    def __get_games(self, days: int) -> dict:
        """
        Queries MLB schedule API to fetch list of future games.
        
        :arg days: Number of days to look ahead when fetching games.
        :returns: dict of mlb games
        """
        today = date.today()
        next_week = today + timedelta(days=days)
        formatted_date_today = today.strftime("%m/%d/%Y")
        formatted_date_future = next_week.strftime("%m/%d/%Y")

        return mlb_api.schedule(
            start_date=formatted_date_today, end_date=formatted_date_future
        )
    
    def __get_location_weather(self):
        pass

    def __get_location(self, game: dict) -> Location:
        """
        Builds location using a game's venue city, state, and country.
        
        :arg game: dict of a single mlb game.
        :returns: Location
        """
        venue_id = game["venue_id"]
        params = {"venueIds": venue_id, "hydrate": "location"}
        venue_info = mlb_api.get(endpoint="venue", params=params)
        loc = venue_info["venues"][0]["location"]
        
        return Location(loc['city'], loc['state'], loc['country'])

    
    def __get_team_ranking(self):
        pass    