from django.contrib import admin
from .models import Tournament, TournamentMatch, TournamentShare

admin.site.register(Tournament)
admin.site.register(TournamentMatch)
admin.site.register(TournamentShare)