# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0


def parse_dialogflow_request(req):
    action = req['queryResult']['action']
    parameters = req['queryResult']['parameters']
    session_token = req['session'].split('/')[-1]
    return session_token, action, parameters
