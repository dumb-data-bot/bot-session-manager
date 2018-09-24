# !/usr/bin/env python3

from abc import ABC, abstractmethod

from keras.utils import data_utils

from utils import dataset_utils


class UserEnv(ABC):

    @abstractmethod
    def list_columns(self):
        pass

    @abstractmethod
    def load_dataset(self, dataset_name):
        # dataset_utils.get_dataset(dataset_name)
        pass

    @abstractmethod
    def get_cols(self):
        pass

    @abstractmethod
    def fill_nas(self, col, mode, val):
        pass

    @abstractmethod
    def show_column(self, col):
        pass

    @abstractmethod
    def choose_predict_target(self, col):
        pass

    @abstractmethod
    def exists_na(self, col):
        pass

    @abstractmethod
    def list_features(self):
        pass

    @abstractmethod
    def add_feature(self, col):
        pass

    @abstractmethod
    def remove_feature(self, col):
        pass
