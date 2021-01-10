from django_filters import rest_framework as filters
from rest_framework import viewsets

from .models import MovieInfo
from .serializers import MovieInfoSerializer


# Create your views here.


class MovieInfoFilter(filters.FilterSet):
    _order = filters.OrderingFilter(
        fields='__all__'
    )

    class Meta:
        model = MovieInfo
        fields = '__all__'


class MovieInfoViewSet(viewsets.ModelViewSet):
    permission_classes = (
    )
    authentication_classes = (
    )
    filterset_class = MovieInfoFilter

    queryset = MovieInfo.objects.all()
    serializer_class = MovieInfoSerializer
