from django.contrib import admin
from django.urls import path
from movies import views

urlpatterns = (
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('rate/', views.rate_movies_view, name='rate_movies'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('search/', views.search_results_view, name='search_movies'),
    path('movie/<int:movie_id>/', views.movie_detail_view, name='movie_detail'),
    path('filter_movies/', views.filter_movies_view, name='filter_movies'),
)

