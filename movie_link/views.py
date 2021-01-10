from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework import viewsets

from .models import MovieInfo
from .serializers import MovieInfoSerializer


class MovieInfoFilter(filters.FilterSet):
    _order = filters.OrderingFilter(
        fields=(
            ('budget', 'Budget'),
            ('revenue', 'Revenue'),
            ('rating', 'Average Rating'),
            ('ratio', 'Budget to revenue ratio'),
            ('title', 'Title'),
            ('year', 'Year'),
        ),
    )

    class Meta:
        model = MovieInfo
        fields = "__all__"


class MovieInfoViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    authentication_classes = ()
    filterset_class = MovieInfoFilter
    queryset = MovieInfo.objects.all()
    serializer_class = MovieInfoSerializer
    filter_backends = (drf_filters.SearchFilter, filters.DjangoFilterBackend)
    search_fields = ["production_companies", "title", "wiki_abstract"]
