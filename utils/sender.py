# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0

from requests import post


class Sender:

    def __init__(self, session_token):
        self.session_token = session_token

    def send(self, event: str, parameters):
        url = 'http://dumbdatabot.appspot.com/backend'
        body = {
            'session': self.session_token,
            'event': event,
            'parameters': parameters,
        }
        print(body)
        post(url, json=body)
