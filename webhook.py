# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0

from flask import Flask, request, make_response, jsonify
from pika import ConnectionParameters, BlockingConnection

from environment import Environment
from session_manager import SessionManager
from utils.composer import Composer
from utils.parser import parse_dialogflow_request

app = Flask(__name__)
log = app.logger

# mq = BlockingConnection(ConnectionParameters(host='localhost'))

env = Environment()


@app.route('/dialogflow', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    log.debug(f'Request: {req}')

    session_token, action, parameters = parse_dialogflow_request(req)

    outcome = env.execute(action, parameters)
    response = {
        'fulfillmentText': outcome,
    }

    # with SessionManager.get_session(session_token, mq) as session:
    #     followup = session.execute(action, parameters)
    # if followup:
    #     event, context = followup
    #     response = Composer.gen_followup_event(event, eval(context))
    # else:
    #     response = req['queryResult']['fulfillmentMessages']
    log.debug(f'Response: {response}')

    return make_response(jsonify(response))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
