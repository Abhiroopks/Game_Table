import json
from datetime import date, datetime, timedelta, timezone

from channels.generic.websocket import WebsocketConsumer
from django.db.models import Max

from games.mlb_generator import MLBGenerator
from games.models import MLBGame

MLB_GENERATOR = MLBGenerator()
NUM_TOP_GAMES = 5


class MLBConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data=None):
        """
        Expects client to send the number of days ahead to fetch games.
        """

        days: int = int(text_data)

        ##
        # Find latest game data in db currently by date
        if MLBGame.objects.count() > 0:
            table_max_date = MLBGame.objects.all().aggregate(Max("date"))["date__max"]
        else:
            table_max_date = date.today()

        max_fetch_date = date.today() + timedelta(days=days)
        tomorrow = date.today() + timedelta(days=1)

        ##
        # Start fetching games from one day AFTER the latest date we currently have in db.
        start_fetch_date = table_max_date + timedelta(days=1)

        ##
        # Only need to fetch new games if we don't already have in db.
        if max_fetch_date > table_max_date:
            MLB_GENERATOR.update_table_data(
                start_day=start_fetch_date, end_day=max_fetch_date
            )

        games = MLBGame.objects.filter(
            date__range=(tomorrow, max_fetch_date + timedelta(days=1))
        ).order_by("win_pct_prod")[:NUM_TOP_GAMES]

        ##
        # Craft list of JSON objects for the games
        games_json: list = []
        for game in games:
            games_json.append(game.to_dict())

        ##
        # Send data to client
        self.send(text_data=json.dumps(games_json))
