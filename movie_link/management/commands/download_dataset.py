"""
Command to reset database to initial state.
"""

from django.core.management import BaseCommand

from movie_link.download import download_dataset


class Command(BaseCommand):
    help = 'Download IMDB movie dataset and WIKI xml zip.'

    def handle(self, *args, **options):
        urls = {
            'wiki': 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz',
            'movies_meta': 'https://storage.googleapis.com/kaggle-data-sets/3405/6663/compressed/movies_metadata.csv.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20210108%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20210108T230157Z&X-Goog-Expires=259199&X-Goog-SignedHeaders=host&X-Goog-Signature=168207d4d4bd6fc8f6fc5dc9b1a5b8ec9527d5cd7e7ec1561d4102c3352bf204db64e9b6f61edfeb5901b4a314a5e59e740b9905a36a6a8b8c96611464cc0fb49b7f7947eb198c06aedb644bdb1bf3b93f3113b32ea84707f9c6d8bf2dc4578a3548d6cc739d813733abb9514d6ecb91c9b85954a2ca13c3a1961887ccc227ecdfcada7348fe3dbf12e4dbc052c7d71f7c111cfcbaee3a4a04d5ad843ba6208051f658f735e705a8e8c06268be78837d82689bb7694513dc7c90fa59b62dccbd0fe255d24a8f9347a0fab6180608375edf9cc27fc63e566f386530f7cc95356c3e98204d0b84b3976abf152bb26ccab4752799e751ecb547d1e12450124624e6'
        }
        download_dataset(urls)
