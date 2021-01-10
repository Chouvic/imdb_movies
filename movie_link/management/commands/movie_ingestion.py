"""
Command to do data ingestion to MovieInfo model.
"""

import pandas as pd
from django.conf import settings
from django.core.management import BaseCommand

from movie_link.models import MovieInfo


def parse_value(func, value):
    try:
        return func(value)
    except ValueError:
        return None


class Command(BaseCommand):
    help = 'Run data ingestion using movie data with link and abstract.'

    def handle(self, *args, **options):
        csv_file_path = settings.DATASET_DIR + 'clean_result_data.csv'
        df = pd.read_csv(csv_file_path)
        for _, row in df.iterrows():
            MovieInfo.objects.get_or_create(
                budget=parse_value(float, row['budget']),
                year=row['year'],
                revenue=parse_value(float, row['revenue']),
                production_companies=row['production_companies'],
                rating=parse_value(float, row['vote_average']),
                ratio=parse_value(float, row['ratio']),
                title=row['title'],
                wiki_url=row['url'],
                wiki_abstract=row['abstract'],
            )
