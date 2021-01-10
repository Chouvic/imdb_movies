from django.db import models


class MovieInfo(models.Model):
    budget = models.FloatField(blank=True, null=True)
    production_companies = models.TextField(blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    ratio = models.FloatField(blank=True, null=True)
    title = models.CharField(max_length=255)
    wiki_url = models.CharField(blank=True, null=True, max_length=1000)
    wiki_abstract = models.TextField(blank=True, null=True, max_length=255)
    year = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return self.title
