from django.db import models


# Create your models here.


class MovieInfo(models.Model):
    budget = models.FloatField()
    production_companies = models.TextField()
    revenue = models.FloatField()
    rating = models.FloatField()
    ratio = models.FloatField()
    title = models.CharField(max_length=255)
    wiki_url = models.CharField(max_length=1000)
    wiki_abstract = models.TextField(max_length=255)
    year = models.CharField(max_length=255)
