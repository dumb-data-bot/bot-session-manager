# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0

import subprocess
from abc import ABC

from pika import BlockingConnection, BasicProperties


class StatefulSession(ABC):

    def __init__(self, session_token: str, mq: BlockingConnection):
        self.session_token = session_token

        self.env_channel = mq.channel()
        self.env_channel.queue_declare(queue=session_token)
        subprocess.Popen([
            'python',
            'work-env/WorkEnv.py',
            session_token,
        ])

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def execute(self, action_name, parameters):
        request_body = f'{action_name}|{parameters}'
        if action_name.endswith('_async'):
            self.env_channel.basic_publish(
                exchange='',
                routing_key=self.session_token,
                body=request_body
            )
        else:
            response = []
            correlation_id = None

            def callback(ch, method, props, response_body):
                if correlation_id == props.correlation_id:
                    response.append(response_body)

            self.env_channel.basic_consume(
                callback,
                queue='amq.rabbitmq.reply-to',
                no_ack=True,
            )

            self.env_channel.basic_publish(
                exchange='',
                routing_key=self.session_token,
                body=request_body,
                properties=BasicProperties(reply_to='amq.rabbitmq.reply-to')
            )

            while not response:
                self.env_channel.connection.process_data_events()
            return response[0].decode().split('|')

    ########################################
    # Data loading
    ########################################
    #
    # # @action
    # def load_dataset(self, dataset_name):
    #     self.env_channel.basic_publish(
    #         routing_key=self.session_token,
    #         body=f'load_dataset|{dataset_name}'
    #     )
    #
    # # @action
    # def download_dataset(self, dataset_name, url):
    #     try:
    #         dataset_utils.fetch(dataset_name, url)
    #     except UserError:
    #         return Composer.gen_followup_event(
    #             Event.DatasetDownloadFailure,
    #             dataset_name=dataset_name,
    #         )
    #     return self.load_dataset(dataset_name)
    #
    # ########################################
    # # Data Exploration
    # ########################################
    #
    # # @action(depends_on=[load_dataset])
    # def list_columns(self):
    #     columns = self.user_env.list_columns()
    #     return Composer.gen_followup_event(
    #         Event.ListColumns,
    #         columns=columns,
    #     )
    #
    # # @action(depends_on=[load_dataset])
    # def show_column(self, col: str):
    #     column_info = self.user_env.show_column(col)
    #     return Composer.gen_followup_event(
    #         Event.ListColumns,
    #         column_info=column_info,
    #     )
    #
    # ########################################
    # # Pre-processing
    # ########################################
    #
    # # @action(depends_on=[load_dataset])
    # def fill_nas(self, col: str, mode: FillNAMode, val: Any = None) -> None:
    #     return self.user_env.fill_nas(col, mode, val)
    #
    # # @action(depends_on=[load_dataset])
    # def encode_col(self, col: str, mode: EncodeMode) -> None:
    #     pass
    #
    # # @action(depends_on=[load_dataset])
    # def normalize_col(self, col: str) -> None:
    #     pass
    #
    # ########################################
    # # Feature Engineering
    # ########################################
    #
    # # @action(depends_on=[load_dataset])
    # def choose_predict_target(self, col: str) -> None:
    #     if self.user_env.exists_na(col):
    #         raise ExistsNaException(col)
    #     self.user_env.choose_predict_target(col)
    #
    # # @action(depends_on=[load_dataset])
    # def list_features(self) -> List[str]:
    #     return self.user_env.list_features()
    #
    # # @action(depends_on=[load_dataset])
    # def add_feature(self, col) -> None:
    #     if self.user_env.exists_na(col):
    #         raise ExistsNaException(col)
    #     return self.user_env.add_feature(col)
    #
    # # @action(depends_on=[load_dataset])
    # def remove_feature(self, col) -> None:
    #     return self.user_env.remove_feature(col)
    #
