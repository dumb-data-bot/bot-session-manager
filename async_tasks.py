# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0

from celery import Celery

from events import Event
from user_env.factory import UserEnvFactory
from utils.sender import Sender

app = Celery(
    'tasks',
    backend='redis://localhost:6379',
    broker='redis://localhost:6379',
)
app.conf.setdefault('CELERY_ACCEPT_CONTENT', ['pickle', 'json'])


@app.task()
def load_dataset(session_token, dataset_name: str):
    user_env = UserEnvFactory.get()
    user_env.load_dataset(dataset_name)
    Sender.send(
        session_token,
        Event.DatasetLoaded,
        dataset_name=dataset_name,
    )
