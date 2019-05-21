# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0

from typing import Dict

from pika import BlockingConnection

from stateful_session import StatefulSession


class SessionManager:
    sessions: Dict[str, StatefulSession] = {}

    @classmethod
    def get_session(cls, session_token: str, mq: BlockingConnection) -> StatefulSession:
        if session_token not in cls.sessions:
            cls.sessions[session_token] = StatefulSession(session_token, mq)
        return cls.sessions.get(session_token)
