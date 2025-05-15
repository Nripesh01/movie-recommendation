"""
URL configuration for movie_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movies.views import (
    home_view,
    register_view,
    login_view,
    logout_view,
    rate_movies_view,
    recommendations_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # 👈 Home page for logged-in users
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('rate/', rate_movies_view, name='rate_movies'),
    path('recommendations/', recommendations_view, name='recommendations'),
]

