# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0

from flask import Flask, request, make_response, jsonify

from session_manager import SessionManager
from utils.parser import parse_dialogflow_request

app = Flask(__name__)
log = app.logger


@app.route('/dialogflow', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    log.debug(f'Request: {req}')

    session_token, action, parameters = parse_dialogflow_request(req)

    with SessionManager.get_session(session_token) as session:
        followup = session.execute(action, parameters)

    response = followup or req['queryResult']['fulfillmentMessages']
    log.debug(f'Response: {response}')

    return make_response(jsonify(response))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
