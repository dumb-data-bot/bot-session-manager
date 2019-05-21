# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0
import sys

from pika import BlockingConnection, ConnectionParameters
from time import sleep
import pandas as pd

from utils.sender import Sender


class WorkEnv:

    def __init__(self, session_token):
        connection = BlockingConnection(ConnectionParameters(host='localhost'))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=session_token)
        self.channel.basic_consume(
            self.consume,
            queue=session_token,
        )
        self.sender = Sender(session_token)
        self.df: pd.DataFrame = None

    def consume(self, ch, method, properties, body):
        action, parameters = body.decode().split('|', 1)
        follow_up = getattr(self, action)(**eval(parameters))
        if follow_up:
            event, parameters = follow_up

            if action.endswith('_async'):
                self.sender.send(event, parameters)
            else:
                ch.basic_publish(
                    '',
                    routing_key=properties.reply_to,
                    body=f'{event}|{parameters}'
                )
        ch.basic_ack(method.delivery_tag)

    def load_dataset_async(self, dataset_name):
        print(f'Loading {dataset_name}')
        self.df = pd.read_csv(f'data/{dataset_name}.csv')
        return 'DatasetLoaded', {'dataset_name': dataset_name}

    def list_columns(self):
        return None, {
            'columns': self.df.columns(),
        }

    def normalize_column(self, column):
        print(f'Normalizing column {column}')
        sleep(1)
        return 'ColumnNormalized', {column: column}


if __name__ == '__main__':
    workspace = WorkEnv(sys.argv[-1])
    workspace.channel.start_consuming()
