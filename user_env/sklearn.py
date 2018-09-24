# !/usr/bin/env python3
from time import sleep

from user_env.base import UserEnv


class SKLearnUserEnv(UserEnv):

    def load_dataset(self, dataset_name):
        sleep(10)

    def list_columns(self):
        pass

    def get_cols(self):
        pass

    def fill_nas(self, col, mode, val):
        pass

    def show_column(self, col):
        pass

    def choose_predict_target(self, col):
        pass

    def exists_na(self, col):
        pass

    def list_features(self):
        pass

    def add_feature(self, col):
        pass

    def remove_feature(self, col):
        pass
