from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>Pygardener</h1>")
