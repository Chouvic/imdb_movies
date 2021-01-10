"""Movie data handler module."""

import logging
import xml.etree.ElementTree as ET

import pandas as pd
from django.conf import settings
from django.template.defaultfilters import slugify

from .utils import parse_value

logger = logging.getLogger("django")

URL_TAG_NAME = 'url'
TITLE_TAG_NAME = 'title'
ABSTRACT_TAG_NAME = 'abstract'


class MovieDataHandle:
    """This class handles CSV operations over IMDB data and WIKI XML file.

    It can be used to extract information from a large XML to get abstract and link.
    """
    _df = None
    _linking_result = None

    def __init__(self, path):
        self.csv_path = path

    @property
    def df(self):
        if self._df is None:
            self._df = pd.read_csv(self.csv_path, encoding="utf-8")
        return self._df

    def add_ratio(self):
        """Calculate the ratio between budget and revenue
        and add the ratio as a column in the dataframe.
        """

        def calculate_ratio(row):
            budget = parse_value(float, row.budget)
            revenue = parse_value(float, row.revenue)
            if not budget or not revenue:
                return None
            return budget / revenue if revenue != 0 else None

        self.df["ratio"] = self.df.apply(calculate_ratio, axis=1)

    def to_csv(self, path):
        self.df.to_csv(path)

    def to_csv_columns(self, path, columns):
        self.df.to_csv(path, columns=columns)

    @property
    def titles_mapping(self):
        # TODO: Title contains duplicate values for about 3188 columns
        #   Think about a way to get unique movie identifier, e.g. imdb_id
        return {
            slugify(item): {"url": None, "abstract": None, "title": item}
            for item in self.df["title"].to_list()
        }

    def match_link_and_abstract(self, xml_file_path):
        """Match link and abstract of each movie.

        This method will match the movie with its wiki link and
        abstract using a large XML.

        To resolve the memory issue, it iterates through the tags
        one by one and deletes the unnecessary tag object for fast performance.
        """
        logger.info("Run XML parsing from %s.", xml_file_path)
        found = False
        pre_title = None
        context = ET.iterparse(xml_file_path)
        titles_mapping = self.titles_mapping
        for event, elem in context:
            if elem.tag == TITLE_TAG_NAME:
                title = slugify(elem.text).replace("wikipedia-", "")
                if title in titles_mapping:
                    found = True
                    pre_title = title
                else:
                    found = False
            if found and elem.tag == URL_TAG_NAME:
                titles_mapping[pre_title][URL_TAG_NAME] = elem.text
            if found and elem.tag == ABSTRACT_TAG_NAME:
                titles_mapping[pre_title][ABSTRACT_TAG_NAME] = elem.text
            elem.clear()
        del context
        logger.info("XML parsing for %s completed.", xml_file_path)

        def serialize_format(mapping):
            # transfer dict results to flat pandas DataFrame and clean data
            _result = pd.DataFrame.from_dict(mapping)
            result_df = _result.T
            result_df["_title"] = result_df.index
            result_df = result_df.reset_index(drop=True)
            del result_df["_title"]
            return result_df

        return serialize_format(titles_mapping)

    def run_movie_matching(self, file_path):
        if self._linking_result is None:
            self._linking_result = self.match_link_and_abstract(file_path)
            self.add_ratio()
            return self._linking_result
        return self._linking_result

    def combine_dfs(self, df2, columns):
        return self.df.merge(df2, how="inner", on=columns)

    @staticmethod
    def sorted_by_ratio(df, column, rows):
        df.sort_values(column, ascending=False)
        return df[:rows]

    @staticmethod
    def save_required_columns_by_ratio(df):
        df.loc[:, "release_date"] = pd.to_datetime(
            df["release_date"], errors="coerce"
        )
        df.loc[:, "year"] = pd.DatetimeIndex(df["release_date"]).year
        required_columns = [
            "title",
            "budget",
            "year",
            "revenue",
            "vote_average",
            "ratio",
            "production_companies",
            "url",
            "abstract",
        ]
        file_name = "clean_result_data.csv"
        file_path = settings.DATASET_DIR + file_name
        df.to_csv(file_path, columns=required_columns)
        logger.info(
            "Saved CSV with columns(%s) to %s.",
            " ".join(required_columns),
            file_path,
        )
