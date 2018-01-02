from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
import pdb

class Hospital(models.Model):
    # Fields
    group = models.OneToOneField(Group, related_name='group', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=60, null=True)
    country = models.CharField(max_length=60, null=True)

    # Representation
    def __str__(self):
        return str(self.group)

class Patient(models.Model):
    # Manifest Constants

    # Martial Status
    SINGLE = 0
    MARRIED = 1
    DIVORCED = 2
    WIDOW = 3
    MARITAL_STATUS = (
        (SINGLE, 'Single'),
        (MARRIED, 'Married'),
        (DIVORCED, 'Divorced'),
        (WIDOW, 'Widow'),
    )

    # Education
    NEVER = 0
    PRIMARY = 1
    SECONDARY = 2
    UNIVERSITY = 3
    EDUCATION_LEVEL = (
        (NEVER, 'Never'),
        (PRIMARY, 'Primary'),
        (SECONDARY, 'Secondary'),
        (UNIVERSITY, 'University'),
    )

    # Fields
    date_created = models.DateTimeField(auto_now_add=True)
    male = models.BooleanField()
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    dob = models.DateField('date of birth')
    age = models.PositiveSmallIntegerField()
    marital_status = models.PositiveSmallIntegerField(
        choices=MARITAL_STATUS,
        default=SINGLE,
    )
    education_level = models.PositiveSmallIntegerField(
        choices=EDUCATION_LEVEL,
        default=NEVER,
    )
    employed = models.BooleanField()
    own_car = models.BooleanField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    # Representation
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Visit(models.Model):
    # Fields
    date_created = models.DateTimeField(auto_now_add=True)
    systolic = models.PositiveSmallIntegerField('systolic pressure', null=True, blank=True)
    diastolic = models.PositiveSmallIntegerField('diastolic pressure', null=True, blank=True)
    weight = models.PositiveSmallIntegerField(null=True, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True)
    bmi = models.PositiveSmallIntegerField(null=True, blank=True)
    waist_circumference = models.PositiveSmallIntegerField(null=True, blank=True)
    total_bc = models.PositiveSmallIntegerField('total blood cholesterol', null=True, blank=True)
    hdl_c = models.PositiveSmallIntegerField('high density hipoprotein cholestrerol', null=True, blank=True)
    fam_card_hist = models.NullBooleanField('family history of cardiovascular disease')
    hypertensive = models.NullBooleanField()
    antihype_med = models.NullBooleanField('on antihypertensive medication')
    new_diag_hype = models.NullBooleanField('newly diagnosed hypertension')
    diabetic = models.NullBooleanField()
    antidiab_med = models.NullBooleanField('on antidiabetic medications')
    bg_fasting = models.PositiveSmallIntegerField('blood glucose fasting', null=True, blank=True)
    bg_random = models.PositiveSmallIntegerField('blood glucose random', null=True, blank=True)
    new_diag_diab = models.NullBooleanField('newly diagnosed diabetes')
    curr_smoker = models.NullBooleanField('current smoker')
    ex_smoker = models.NullBooleanField()
    alcohol_misuse = models.NullBooleanField()
    premature_menopause = models.NullBooleanField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    # Representation
    def __str__(self):
        return 'Visit on %s made by %s' % (self.date_created, self.patient)

@receiver(models.signals.post_delete, sender=Hospital)
def handle_deleted_hospital(sender, instance, **kwargs):
    """
    deletes the associated group of a hospital upon hospital deletion
    """
    instance.group.delete()
