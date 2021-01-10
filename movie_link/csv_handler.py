import logging
import xml.etree.ElementTree as ET

import pandas as pd
from django.conf import settings
from django.template.defaultfilters import slugify

logger = logging.getLogger("django")


class MovieDataParse:
    _df = None
    _linking_result = None

    def __init__(self, path):
        self.csv_path = path

    @property
    def df(self):
        if self._df is None:
            self._df = pd.read_csv(self.csv_path, encoding="utf-8")
        return self._df

    @staticmethod
    def parse_float(value):
        try:
            result = float(value)
            return result
        except ValueError:
            return None

    def add_ratio(self):
        """Calculate the ratio between budget and revenue.

        @reviewer Another way is to convert all values to float and use default div in pandas
        The following can preserve the information of inf(Recorded when divided by zero).

        # df["budget"] = pd.to_numeric(df["budget"], errors='coerce', downcast="float")
        # df["revenue"] = pd.to_numeric(df["revenue"], errors='coerce', downcast="float")
        # df['budget_revenue_ratio'] = df.budget / df.revenue

        However, the above approach needs to handle to_csv export as index
        over NAN values is deprecated.

        """

        def calculate_ratio(row):
            budget = self.parse_float(row.budget)
            revenue = self.parse_float(row.revenue)
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
        """Match link and abstract of each movie."""
        logger.info("Run XML parsing from %s.", xml_file_path)
        found = False
        pre_title = None
        context = ET.iterparse(xml_file_path)
        titles_mapping = self.titles_mapping
        for event, elem in context:
            if elem.tag == "title":
                title = slugify(elem.text).replace("wikipedia-", "")
                if title in titles_mapping:
                    found = True
                    pre_title = title
                else:
                    found = False
            if found and elem.tag == "url":
                titles_mapping[pre_title]["url"] = elem.text
            if found and elem.tag == "abstract":
                titles_mapping[pre_title]["abstract"] = elem.text
            elem.clear()
        del context
        logger.info("XML parsing for %s completed.", xml_file_path)

        def serialize_format(mapping):
            _result = pd.DataFrame.from_dict(mapping)
            result_df = _result.T
            result_df["_title"] = result_df.index
            result_df = result_df.reset_index(drop=True)
            del result_df["_title"]
            return result_df

        return serialize_format(titles_mapping)

    def run_match_and_combine(self, file_path):
        if self._linking_result is None:
            self._linking_result = self.match_link_and_abstract(file_path)
            self.add_ratio()
            return self._linking_result
        return self._linking_result

    def combine_dfs(self, df2, columns):
        combined_df = self.df.merge(df2, how="inner", on=columns)
        combined_df_name = "movies_ratio_link.csv"
        combined_df.to_csv(settings.DATASET_DIR + combined_df_name)
        return combined_df

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
        # df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        # df['year'] = pd.DatetimeIndex(df['release_date']).year
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
