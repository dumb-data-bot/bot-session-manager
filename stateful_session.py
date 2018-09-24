# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0

from abc import ABC
from typing import List, Any

import async_tasks
from events import Event
from user_env.factory import UserEnvFactory
from user_env.base import UserEnv


# def action(depends_on: List[Callable] = ()):
#     """Treats decorated methods as action events.
#
#     Dependencies are checked against executed events history.
#     Execution will be logged once complete.
#     """
#
#     def wrap(func):
#         @functools.wraps(func)
#         def _impl(self, *args, **kwargs):
#             for depends_on_action in depends_on:
#                 if depends_on_action not in self.action_set:
#                     raise errors.RequirementUnfulfilledError(action)
#             result = func(self, *args, **kwargs)
#             self.actions.append(func, args, kwargs)
#             return result
#
#         return _impl
#
#     return wrap
from utils import dataset_utils
from utils.composer import Composer
from utils.errors import UserError, ExistsNaException
from utils.types import FillNAMode, EncodeMode


class StatefulSession(ABC):

    def __init__(self, session_token: str):
        self.session_token = session_token

        # self.action_list: List[Tuple[Callable, List[Any], Dict[str, Any]]] = []
        # self.action_set: Set[Callable] = set()
        self.user_env: UserEnv = UserEnvFactory.get()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def execute(self, action_name, parameters):
        return getattr(self, action_name)(**parameters)

    ########################################
    # Data loading
    ########################################

    # @action
    def load_dataset(self, dataset_name):
        if not dataset_utils.exists(dataset_name):
            return Composer.gen_followup_event(
                Event.DatasetNotExists,
                dataset_name=dataset_name,
            )
        async_tasks.load_dataset.delay(
            self.session_token,
            dataset_name,
        )

    # @action
    def download_dataset(self, dataset_name, url):
        try:
            dataset_utils.fetch(dataset_name, url)
        except UserError:
            return Composer.gen_followup_event(
                Event.DatasetDownloadFailure,
                dataset_name=dataset_name,
            )
        return self.load_dataset(dataset_name)

    ########################################
    # Data Exploration
    ########################################

    # @action(depends_on=[load_dataset])
    def list_columns(self):
        columns = self.user_env.list_columns()
        return Composer.gen_followup_event(
            Event.ListColumns,
            columns=columns,
        )

    # @action(depends_on=[load_dataset])
    def show_column(self, col: str):
        column_info = self.user_env.show_column(col)
        return Composer.gen_followup_event(
            Event.ListColumns,
            column_info=column_info,
        )

    ########################################
    # Pre-processing
    ########################################

    # @action(depends_on=[load_dataset])
    def fill_nas(self, col: str, mode: FillNAMode, val: Any = None) -> None:
        return self.user_env.fill_nas(col, mode, val)

    # @action(depends_on=[load_dataset])
    def encode_col(self, col: str, mode: EncodeMode) -> None:
        pass

    # @action(depends_on=[load_dataset])
    def normalize_col(self, col: str) -> None:
        pass

    ########################################
    # Feature Engineering
    ########################################

    # @action(depends_on=[load_dataset])
    def choose_predict_target(self, col: str) -> None:
        if self.user_env.exists_na(col):
            raise ExistsNaException(col)
        self.user_env.choose_predict_target(col)

    # @action(depends_on=[load_dataset])
    def list_features(self) -> List[str]:
        return self.user_env.list_features()

    # @action(depends_on=[load_dataset])
    def add_feature(self, col) -> None:
        if self.user_env.exists_na(col):
            raise ExistsNaException(col)
        return self.user_env.add_feature(col)

    # @action(depends_on=[load_dataset])
    def remove_feature(self, col) -> None:
        return self.user_env.remove_feature(col)

