# movies/admin.py

from django.contrib import admin
from .models import Movie, Rating

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'year')  # customize columns

admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating)
