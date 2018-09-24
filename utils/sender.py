# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0

from requests import post

from events import Event


class Sender:

    @staticmethod
    def send(session_token: str, event: Event, **parameters):
        # url = 'http://localhost:6677/backend'
        url = 'https://dumbdatabot.appspot.com/backend'
        body = {
            'session': session_token,
            'event': event.value,
            'parameters': parameters,
        }

        post(url, json=body)
