import gzip
import io
import logging
import shutil
import zipfile
from pathlib import Path

import requests
from django.conf import settings

logger = logging.getLogger("django")


def download_helper(url, file_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }

    res = requests.get(url, allow_redirects=True, headers=headers)
    with open(file_path, "wb") as file:
        file.write(res.content)


def download_wiki_file(url_path):
    """Download and extract WIKI XML file."""
    wiki_file_name = url_path.rsplit("/", 1)[1]
    wiki_path = settings.DATASET_DIR + wiki_file_name
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    logger.info("WIKI XML file is being downloaded.")
    res = requests.get(url_path, allow_redirects=True, headers=headers)
    with open(wiki_path, "wb") as file:
        file.write(res.content)
    logger.info("WIKI XML file saved.")
    extract_gz_file(wiki_path)


def extract_gz_file(file_path):
    logger.info("File %s is being extracted.", file_path)
    new_file_path = file_path.replace(".gz", "")
    with gzip.open(file_path, "rb") as f_in:
        with open(new_file_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    logger.info("File has been extracted to %s.", new_file_path)


def download_movie_data(data_url):
    logger.info("IMDB metadata is being downloaded.")
    r = requests.get(data_url, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(settings.DATASET_DIR)
    logger.info("IMDB metadata file saved.")


def download_dataset(urls):
    logger.info("Started dataset downloading jobs.")
    Path(settings.DATASET_DIR).mkdir(parents=True, exist_ok=True)
    download_movie_data(urls["movies_meta"])
    download_wiki_file(urls["wiki"])
    logger.info("All dataset downloaded and saved.")


if __name__ == "__main__":
    urls = {
        "wiki": "https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz",
        "movies_meta": "https://storage.googleapis.com/kaggle-data-sets/3405/6663/compressed/movies_metadata.csv.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20210108%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20210108T230157Z&X-Goog-Expires=259199&X-Goog-SignedHeaders=host&X-Goog-Signature=168207d4d4bd6fc8f6fc5dc9b1a5b8ec9527d5cd7e7ec1561d4102c3352bf204db64e9b6f61edfeb5901b4a314a5e59e740b9905a36a6a8b8c96611464cc0fb49b7f7947eb198c06aedb644bdb1bf3b93f3113b32ea84707f9c6d8bf2dc4578a3548d6cc739d813733abb9514d6ecb91c9b85954a2ca13c3a1961887ccc227ecdfcada7348fe3dbf12e4dbc052c7d71f7c111cfcbaee3a4a04d5ad843ba6208051f658f735e705a8e8c06268be78837d82689bb7694513dc7c90fa59b62dccbd0fe255d24a8f9347a0fab6180608375edf9cc27fc63e566f386530f7cc95356c3e98204d0b84b3976abf152bb26ccab4752799e751ecb547d1e12450124624e6",
    }
    download_dataset(urls)
