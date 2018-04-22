from django.db import models
import uuid


class Email(models.Model):
    email = models.CharField(max_length=254)

    def __str__(self):
        return self.email


class Subscriber(models.Model):
    # longest emails are 254: https://stackoverflow.com/a/7717596/2965993
    # email = models.CharField(max_length=254, unique=True)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    verify_guid = models.CharField(max_length=36, default=str(uuid.uuid4()))
    registered = models.DateTimeField(auto_now_add=True)
    # US zips are 5 chars
    zip_code = models.CharField(max_length=5)
    curses = models.BooleanField(default=False)
    subscribe = models.BooleanField(default=False)

    def __str__(self):
        return self.email.email
