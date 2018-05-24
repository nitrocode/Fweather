from django.apps import AppConfig
from fweather.external.sendemail import Gmail
import logging

logger = logging.getLogger(__name__)


class FweatherConfig(AppConfig):
    name = 'fweather'

    def ready(self):
        # check or get the token on boot
        logger.info("GMAIL: Get refresh token...")
        try:
            Gmail()
            logger.info("GMAIL: ...DONE")
        except:
            logger.info("GMAIL: ...FAIL")
