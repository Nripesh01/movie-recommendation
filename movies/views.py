from django.shortcuts import render, redirect
from .recommender import get_recommendations_for_user
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.contrib.auth.models import User
import pandas as pd
from .models import Rating, Movie
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .form import RegisterForm  
from django.template.defaulttags import register

# jwfeffsdksdjlsdf
def    recommendations_view(request):

    user = request.user

    # Load ratings from the database
    ratings_qs = Rating.objects.all().values('user_id', 'movie_id', 'rating')
    df = pd.DataFrame(ratings_qs)

    # Handle case when no ratings exist or if the user hasn't rated any movie
    if df.empty or user.id not in df['user_id'].unique():
        return render(request, 'movies/recommendations.html', {
            'recommendations': [],
            'message': 'Not enough data to generate recommendations.'
        })

    # Create user-movie matrix
    rating_matrix = df.pivot_table(index='user_id', columns='movie_id', values='rating').fillna(0)

    # Compute cosine similarity between users
    user_sim = cosine_similarity(rating_matrix)
    user_sim_df = pd.DataFrame(user_sim, index=rating_matrix.index, columns=rating_matrix.index)

    # Get similarities for the current user (exclude themselves)
    if user.id not in user_sim_df.index:
        return render(request, 'movies/recommendations.html', {
            'recommendations': [],
            'message': 'You have not rated any movies yet.'
        })

    sim_scores = user_sim_df.loc[user.id].drop(user.id)
    similar_users = sim_scores[sim_scores > 0]

    # If no similar users, return early
    if similar_users.empty:
        return render(request, 'movies/recommendations.html', {
            'recommendations': [],
            'message': 'No similar users found for recommendations.'
        })

    # Get ratings from similar users
    aligned_ratings = rating_matrix.loc[similar_users.index]

    # Multiply each user's ratings by their similarity score
    ratings_matrix_np = aligned_ratings.to_numpy().T  # shape: (movies, users)
    sim_weights_np = similar_users.to_numpy()         # shape: (users,)

    weighted_scores = ratings_matrix_np.dot(sim_weights_np)
    sim_sum = sim_weights_np.sum() or 1e-9  # avoid division by zero
    final_scores = weighted_scores / sim_sum

    # Convert results to Series with movie IDs as index
    movie_ids = aligned_ratings.columns
    scores_series = pd.Series(final_scores, index=movie_ids).sort_values(ascending=False)

    # Filter out movies already rated by the user
    already_rated = set(df[df['user_id'] == user.id]['movie_id'])
    recommended_movie_ids = [mid for mid in scores_series.index if mid not in already_rated][:10]

    recommended_movies = Movie.objects.filter(id__in=recommended_movie_ids)

    return render(request, 'movies/recommendations.html', {
        'recommendations': recommended_movies,
        'message': None if recommended_movies else 'No new recommendations found.'
    })

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('home')  # Redirect to home page after login
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'movies/login.html', {'form': form})


# Register View
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to login page after registration
    else:
        form = RegisterForm()

    return render(request, 'movies/register.html', {'form': form})

@login_required
def rate_movies_view(request):
    movies = Movie.objects.all()

    if request.method == 'POST':
        for movie in movies:
            rating_val = request.POST.get(f'rating_{movie.id}')
            if rating_val:
                rating_obj, created = Rating.objects.update_or_create(
                    user=request.user,
                    movie=movie,
                    defaults={'rating': rating_val}
                )
        messages.success(request, "Ratings submitted successfully!")
        return redirect('recommendations')

    user_rated = Rating.objects.filter(user=request.user)
    user_ratings = {r.movie.id: r.rating for r in user_rated}

    return render(request, 'movies/rate_movies.html', {
        'movies': movies,
        'user_ratings': user_ratings,
    })


def home_view(request):
    return render(request, 'movies/home.html')


def get_item(dictionary, key):
    return dictionary.get(key)


def logout_view(request):
    logout(request)
    return redirect('login')