from django.apps import AppConfig
from fweather.external.sendemail import Gmail


class FweatherConfig(AppConfig):
    name = 'fweather'

    def ready(self):
        # check or get the token on boot
        print("GMAIL: Get refresh token...")
        try:
            gmail = Gmail()
            print("GMAIL: ...DONE")
        except:
            print("GMAIL: ...FAIL")
