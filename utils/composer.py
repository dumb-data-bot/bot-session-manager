# !/usr/bin/env python3
# Copyright: Jun Zhang (jzhang@comp.nus.edu.sg)
# Licence: Apache Licence 2.0

from events import Event


class Composer:

    @staticmethod
    def gen_followup_event(event: Event, **parameters):
        return {
            'followupEventInput': {
                'name': event.value,
                'parameters': parameters,
                'languageCode': 'en-US',
            }
        }
