# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0

from enum import Enum


class Event(Enum):
    DatasetLoaded = 'DatasetLoaded'
    DatasetNotExists = 'DatasetNotExists'
    DatasetDownloadFailure = 'DatasetDownloadFailure'
