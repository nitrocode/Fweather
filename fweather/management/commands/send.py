from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from fweather.models import Subscriber, Email
from fweather.external.sendemail import Gmail
from fweather.external import weather
from fweather.external import giphy
import zipcodes
import asyncio
import time
import logging


class Command(BaseCommand):
    help = 'Send fun weather emails'

    def __init__(self):
        super(Command, self).__init__()
        # init the gmail object
        self.gmail = Gmail()

    def add_arguments(self, parser):
        """Add basic args to send command."""
        parser.add_argument('--email', help='Send to a particular email')
        parser.add_argument(
            '--email-all',
            action="store_true",
            default=False,
            help='Send to all emails in database')

    def handle(self, *args, **options):
        """Handle my subscribers.

        :param args: standard, see add_arguments for more details
        :param options: standard, see add_arguments for more details
        :return: NOTHING
        """
        # this if is checked twice
        email_all = 'email_all' in options and options['email_all']
        subscribers = []
        if 'email' in options:
            # if just one email, filter for it
            email = Email.objects.get(email=options['email'])
            # make sure the email exists in Subscriber table and subscribe is True
            if email:
                try:
                    subscribers = [
                        Subscriber.objects.get(email=email, subscribe=True)
                    ]
                except ObjectDoesNotExist:
                    logging.info('Subscriber found but they have not verified '
                                 'their email or chose to unsubscribe.')
        elif email_all:
            # run through all the subscribers on the list
            subscribers = Subscriber.objects.filter(subscribe=True)

        # do nothing if no subscribers
        if len(subscribers) == 0:
            logging.info("No verified subscribers found.")
            return
        elif email_all:
            # Avoid accidents if emailing all
            cont = input(
                'Are you sure you want to email {} people? [N]/y '.format(
                    len(subscribers)))

            if not cont.lower() == 'y':
                logging.info("User exited")
                return

        # Time this
        start = time.time()

        # make it all async so it's fast
        loop = asyncio.get_event_loop()
        tasks = []
        for sub in subscribers:
            tasks.append(self.send(sub))
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

        logging.info('Total time: {}'.format(time.time() - start))

    async def send(self, sub):
        """Send a weather email with a gif to a subscriber.

        :param sub: Subscriber object
        :return: NOTHING
        """
        discount = 'enjoy a discount on us.'
        zip_code = sub.zip_code
        data = weather.search(zip_code)
        loc = zipcodes.matching(zip_code)[0]
        mean = weather.get_yearly_average_temp(data)
        current = weather.get_current_temp(data)
        icon = weather.get_current_weather_icon(data)
        desc = weather.get_current_weather_desc(data)
        gif = giphy.get_random_giphy(desc)
        if current >= mean + 5:
            subject = 'It\'s nice out! {}'.format(discount.capitalize())
        elif current <= mean - 5 or weather.is_raining(data):
            subject = 'Not so nice out? That\'s okay, {}'.format(discount)
        else:
            subject = discount.title()
        # TODO: attach gif
        body = """
            <img src="{}"><br /><br />
            ZIP: {}<br />
            Location: {}, {}<br />
            Weather: {} °{}<br /><br />
            <img src="{}"><br /><br />
        """.format(icon, zip_code, loc['city'], loc['state'], current, 'F',
                   gif)
        self.gmail.send(sub.email.email, subject, body)
        logging.info(sub.email.email)
        logging.info(body)
