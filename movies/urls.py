from django.contrib import admin
from django.urls import path
from movies.views import (
    register_view,
    login_view,
    logout_view,
    rate_movies_view,
    home_view,
    recommendations_view,  
)

urlpatterns = (
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('rate/', rate_movies_view, name='rate_movies'),
    path('recommendations/', recommendations_view, name='recommendations'),
)
