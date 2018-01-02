from django.contrib import admin

from .models import Hospital, Patient, Visit

admin.site.register(Hospital)
admin.site.register(Patient)
admin.site.register(Visit)
