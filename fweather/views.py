from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from fweather.models import Subscriber, Email
from fweather.external.sendemail import Gmail
import logging
# validators
from email_validator import validate_email, EmailNotValidError
import zipcodes


class HomePageView(TemplateView):
    template_name = 'signup.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'


def sign_up(request):
    data = {'success': False}
    email = request.POST['email_name'].lower()
    zip_code = request.POST['zip_code_name']
    # validate email
    try:
        valid = validate_email(email)
        email = valid["email"]
    except EmailNotValidError:
        data['msg'] = 'Email is invalid'
        return JsonResponse(data)
    # validate zip
    match = zipcodes.matching(zip_code)
    if not match:
        data['msg'] = 'Zip code is invalid'
        return JsonResponse(data)
    # default curses to False if not submitted
    if 'curses_name' in request.POST:
        curses = request.POST['curses_name']
    else:
        curses = False
    try:
        # if email does not exist, then add it
        new_email, created = Email.objects.get_or_create(
            email=email, defaults={'email': email})
        # created = True
        # if email is created, then
        if created:
            logging.info('created email {}'.format(email))
            # add subscriber
            sub, created = Subscriber.objects.get_or_create(
                email=new_email,
                zip_code=zip_code,
                curses=curses,
            )
            gmail = Gmail()
            # verify email
            gmail.send(
                email,
                'Verify your email for Fweather!',
                'Click <a href="{}/verify?id={}">here</a> to verify!'.format(
                    request.build_absolute_uri(), sub.verify_guid),
            )
            logging.info('email sent')
        else:
            logging.info('not created')
    except IntegrityError:
        # This error was thrown when a duplicate was found.
        # Set defaults on email to avoid this.
        # Reference: https://stackoverflow.com/q/19362085/2965993
        pass
    data['success'] = True
    data['msg'] = 'Subscribed email successfully for {} {}!'.format(
        match[0]['city'], match[0]['state'])
    return JsonResponse(data)


def verify(request):
    guid = request.GET['id']
    msg = "Already verified!"
    try:
        sub = Subscriber.objects.get(verify_guid=guid)
        if not sub.subscribe:
            msg = "Verified {}".format(sub.email.email)
            sub.subscribe = True
            sub.save()
    except ObjectDoesNotExist:
        pass
    return HttpResponse(msg)
