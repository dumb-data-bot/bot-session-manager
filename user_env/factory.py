# !/usr/bin/env python3

from user_env.base import UserEnv
from user_env.sklearn import SKLearnUserEnv


class UserEnvFactory:

    @staticmethod
    def get() -> UserEnv:
        return SKLearnUserEnv()
