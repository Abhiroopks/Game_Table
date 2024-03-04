
from django.shortcuts import render

from games.mlb_generator import MLBGenerator
from games.models import MLBGame

MLB_GENERATOR = MLBGenerator()


def index(request):
    MLB_GENERATOR.update_table_data(1)
    mlb_games = MLBGame.objects.all()
    context = {
        "mlb_games": mlb_games
    }
    
    return render(request=request, template_name="games/index.html", context=context)