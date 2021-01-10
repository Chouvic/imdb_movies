from django.urls import include, path
from rest_framework.routers import DefaultRouter

from movie_link import views

router = DefaultRouter()

router.register(r'movies', views.MovieInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
