# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0


class Composer:

    @staticmethod
    def gen_followup_event(event: str, parameters):
        return {
            'followupEventInput': {
                'name': event,
                'parameters': parameters,
                'languageCode': 'en-US',
            }
        }
