from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField()
    poster_url = models.URLField(blank=True)
    release_year = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
       return f"{self.user.username} - {self.movie.title} - {self.rating}"