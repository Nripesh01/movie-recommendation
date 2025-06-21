import requests
from django.conf import settings

BASE_URL = 'https://api.themoviedb.org/3'

def search_movies(query):
    url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': settings.TMDB_API_KEY,
        'query': query,
        'language': 'en-US',
        'page': 1,
        'include_adult': False
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': settings.TMDB_API_KEY,
        'language': 'en-US'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None
