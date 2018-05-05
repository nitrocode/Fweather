from django.apps import AppConfig
from fweather.external.sendemail import Gmail
import logging


class FweatherConfig(AppConfig):
    name = 'fweather'

    def ready(self):
        # check or get the token on boot
        logging.info("GMAIL: Get refresh token...")
        try:
            gmail = Gmail()
            logging.info("GMAIL: ...DONE")
        except:
            logging.info("GMAIL: ...FAIL")
