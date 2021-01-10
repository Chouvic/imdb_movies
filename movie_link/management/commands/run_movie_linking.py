"""
Command to run the movie data linking and save results to CSV.
"""

from django.conf import settings
from django.core.management import BaseCommand

from movie_link.csv_handler import MovieDataHandle


class Command(BaseCommand):
    help = "Download IMDB movie dataset and WIKI xml zip."

    def handle(self, *args, **options):
        movie_parse = MovieDataHandle(
            settings.DATASET_DIR + "movies_metadata.csv"
        )
        xml_filepath = settings.DATASET_DIR + "enwiki-latest-abstract.xml"
        match_result = movie_parse.run_movie_matching(xml_filepath)
        combine_df = movie_parse.combine_dfs(match_result, ["title"])
        sorted_df = movie_parse.sorted_by_ratio(combine_df, "ratio", 1000)
        movie_parse.save_required_columns_by_ratio(sorted_df)
