from datetime import date
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
    def update_table_data(self, start_day: date, end_day: date):
        """
        Queries schedule and weather api to generate table data.
        
        :arg start_day: First day of games to include
        :arg end_day: Last day of games to include
        :returns: None
        """
        games = self.__get_games(start_day=start_day, end_day=end_day)
        for game in games:
            game_record: MLBGame = MLBGame()
            game_record.id = game["game_id"]
            game_record.datetime = game["game_datetime"]
            game_record.home_team = game["home_name"]
            game_record.away_team = game["away_name"]
            
            location: Location = self.__get_location(game)
            game_record.location = location.get_query()
            
            game_record.save()
            
            
        
        
    
    def __get_games(self, start_day: date, end_day: date) -> dict:
        """
        Queries MLB schedule API to fetch list of future games over specified range of dates.
        
        :arg start_day: First day of games to include
        :arg end_day: Last day of games to include
        :returns: dict of mlb games
        """
        formatted_date_start = start_day.strftime("%m/%d/%Y")
        formatted_date_end = end_day.strftime("%m/%d/%Y")

        return mlb_api.schedule(
            start_date=formatted_date_start, end_date=formatted_date_end
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