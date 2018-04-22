from django.contrib import admin
from .models import Subscriber, Email


class EmailAdmin(admin.ModelAdmin):
    raw_id_fields = ("email",)


admin.site.register(Subscriber)
admin.site.register(Email)
