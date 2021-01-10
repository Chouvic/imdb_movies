from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework import viewsets

from .models import MovieInfo
from .serializers import MovieInfoSerializer


# Create your views here.


class MovieInfoFilter(filters.FilterSet):
    class Meta:
        model = MovieInfo
        fields = '__all__'


class MovieInfoViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    authentication_classes = ()
    filterset_class = MovieInfoFilter
    queryset = MovieInfo.objects.all()
    serializer_class = MovieInfoSerializer
    filter_backends = (drf_filters.SearchFilter, filters.DjangoFilterBackend)
    search_fields = ['production_companies', 'title', 'wiki_abstract']
