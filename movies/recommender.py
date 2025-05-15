import pandas as pd
from movies.models import Rating, Movie
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_user_movie_matrix():
    ratings = Rating.objects.all().select_related('movie', 'user')
    
    data = []
    for r in ratings:
        data.append({
            'user_id': r.user.id,
            'movie_title': r.movie.title,
            'rating': r.rating
        })

    df = pd.DataFrame(data)
    user_movie_matrix = df.pivot_table(index='user_id', columns='movie_title', values='rating')
    return user_movie_matrix



def get_recommendations_for_user(user_id, top_n=5):
    matrix = get_user_movie_matrix()
    matrix_filled = matrix.fillna(0)

    if user_id not in matrix_filled.index:
        return []

    similarity = cosine_similarity(matrix_filled)
    sim_df = pd.DataFrame(similarity, index=matrix_filled.index, columns=matrix_filled.index)

    user_similarities = sim_df[user_id].sort_values(ascending=False)[1:]

    weighted_scores = np.dot(user_similarities.values, matrix_filled.loc[user_similarities.index])
    mean_ratings = matrix_filled.mean(axis=0)
    
    scores = pd.Series(weighted_scores, index=matrix_filled.columns)
    unseen = matrix.loc[user_id][matrix.loc[user_id].isnull()].index
    recommendations = scores[unseen].sort_values(ascending=False).head(top_n)

    return list(recommendations.index)
