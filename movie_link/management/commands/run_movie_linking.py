"""
Command to reset database to initial state.
"""

import time

from django.conf import settings
from django.core.management import BaseCommand

from movie_link.csv_handler import MovieDataParse


class Command(BaseCommand):
    help = 'Download IMDB movie dataset and WIKI xml zip.'

    def handle(self, *args, **options):
        start = time.time()
        movie_parse = MovieDataParse(settings.DATASET_DIR + 'movies_metadata.csv')
        xml_filepath = settings.DATASET_DIR + 'enwiki-latest-abstract.xml'
        match_result = movie_parse.run_match_and_combine(xml_filepath)
        combine_df = movie_parse.combine_dfs(match_result, ['title'])
        sorted_df = movie_parse.sorted_by_ratio(combine_df, 'ratio', 1000)
        movie_parse.save_required_columns_by_ratio(sorted_df)
        print(sorted_df.head())
        end = time.time()
        print(end - start)
