from datetime import date

import statsapi as mlb_api

from games.models import MLBGame

GAME_TYPES = {
    "S": "Spring Training",
    "R": "Regular Season",
    "F": "Wild Card Game",
    "D": "Division Series",
    "L": "League Championship Series",
    "W": "World Series",
    "C": "Championship",
    "N": "Nineteenth Century Series",
    "P": "Playoffs",
    "A": "All-Star Game",
    "I": "Intrasquad",
    "E": "Exhibition",
}


class Location:
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


class MLBGenerator:
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
        standings = self.__get_standings()
        for game in games:
            game_record: MLBGame = MLBGame()
            game_record.id = game["game_id"]
            game_record.date = game["game_date"]
            game_record.game_type = GAME_TYPES[game["game_type"]]
            game_record.home_team = game["home_name"]
            game_record.away_team = game["away_name"]

            ##
            # Loc data
            location: Location = self.__get_location(game)
            game_record.location = location.get_query()

            ##
            # Standings data
            game_record.home_win_pct = standings[game_record.home_team]["win_pct"]
            game_record.away_win_pct = standings[game_record.away_team]["win_pct"]

            ##
            # Win Pct Product: a metric to measure combined win pct of teams.
            # Higher nums = better matchup. (better teams playing eachother)
            game_record.win_pct_prod = (
                game_record.home_win_pct * game_record.away_win_pct
            )

            game_record.save()

    def __get_standings(self) -> dict:
        standings = mlb_api.standings_data()
        ##
        # Maps team_name -> Standings data
        standings_final = {}
        for div_data in standings.values():
            for team in div_data["teams"]:
                try:
                    win_pct = (team["w"]) / (team["w"] + team["l"])
                except ZeroDivisionError:
                    win_pct = 1

                team_data = {
                    "win_pct": win_pct,
                    "league_rank": team["league_rank"],
                    "div_name": div_data["div_name"],
                }

                standings_final[team["name"]] = team_data

        return standings_final

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

        return Location(
            loc.get("city", ""), loc.get("state", ""), loc.get("country", "")
        )
