# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0

import pandas as pd
from requests import get

from utils.errors import InvalidDatasetUrl


def _to_path(dataset_name):
    return dataset_name


def get_dataset(dataset_name) -> pd.DataFrame:
    return pd.read_csv(_to_path(dataset_name))


def fetch(dataset_name, url) -> None:
    with open(_to_path(dataset_name), 'w') as file:
        with get(url) as response:
            if response.status_code != 200:
                raise InvalidDatasetUrl()
            file.write(response.content)


def exists(dataset_name: str) -> bool:
    return True
