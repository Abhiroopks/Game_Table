from django.shortcuts import render


def index(request):
    return render(request=request, template_name="games/index.html")
