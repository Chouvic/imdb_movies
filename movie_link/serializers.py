from rest_framework.serializers import ModelSerializer

from movie_link.models import MovieInfo


class MovieInfoSerializer(ModelSerializer):
    class Meta:
        model = MovieInfo
        fields = '__all__'
