from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta


COMMON_TITLES = [('Ms', 'Ms'),
                 ('Miss', 'Miss'),
                 ('Mrs', 'Mrs'),
                 ('Mr', 'Mister'),
                 ('Master', 'Master'),
                 ('Rev', 'Reverend'),
                 ('Fr', 'Father'),
                 ('Dr', 'Doctor'),
                 ('Prof', 'Professor'),
                 ('Hon', 'Honor'),
                 ('Pres', 'President'),
                 ('Gov', 'Govenor')]

ADDRESS_RELS = [(0, 'Other'), (1, 'Home'), (2, 'Work')]

PHONE_RELS = [(0, 'Assistant'),
              (1, 'Callback'),
              (2, 'Car'),
              (3, 'Company Main'),
              (4, 'Fax'),
              (5, 'ISDN'),
              (6, 'Main'),
              (7, 'Mobile'),
              (8, 'Other'),
              (9, 'Other (Fax)'),
              (10, 'Pager'),
              (11, 'Radio'),
              (12, 'Telex'),
              (13, 'TTY TTD'),
              (14, 'Work'),
              (15, 'Work (Fax)'),
              (16, 'Work (Mobile)'),
              (17, 'Work (Pager)')]

STATES = [('QLD','Queensland'),
          ('NSW', 'New South Wales'),
          ('VIC', 'Victoria'),
          ('TAS', 'Tasmania'),
          ('WA', 'Western Australia'),
          ('SA', 'South Australia'),
          ('ACT', 'Australian Capitol Territory'),
          ('NT', 'Northern Territory')]


class StaffMember(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    title = models.CharField(max_length=50, choices=COMMON_TITLES)
    prefered_given_name = models.CharField(max_length=255, blank=True, null=True)
    legal_given_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    prefered_surname = models.CharField(max_length=255, blank=True, null=True)
    legal_surname = models.CharField(max_length=255)
    # addresses back reference
    # phone_numbers back reference
    # email_addresses back reference
    dob = models.DateField()
    religion = models.CharField(max_length=255)
    teacher_registration_number = models.IntegerField(unique=True, blank=True, null=True)
    teacher_registration_expiry = models.DateField(blank=True, null=True)
    # subjects taught
    timetable_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    employee_number = models.CharField(max_length=255, unique=True)
    bluecard_number = models.CharField(max_length=255, unique=True)
    bluecard_expiry = models.DateField()
    # next_of_kin back reference
    vehicle_registration = models.CharField(max_length=50, blank=True, null=True)
    media_consent_form = models.BooleanField(default=False)
    weekly_hours_worked = models.IntegerField(default=38)
    works_monday = models.BooleanField(default=True)
    works_tuesday = models.BooleanField(default=True)
    works_wednesday = models.BooleanField(default=True)
    works_thursday = models.BooleanField(default=True)
    works_friday = models.BooleanField(default=True)
    # qualifications back reference
    active = models.BooleanField(default=True)

    @property
    def display_name(self):
        first_name = self.prefered_given_name or self.legal_given_name
        last_name = self.prefered_surname or self.legal_surname
        return '{} {} {}'.format(self.title, first_name, last_name)

    @property
    def valid_bluecard(self):
        if self.bluecard_expiry > date.today():
            return True
        else:
            return False

    @property
    def age(self):
        return relativedelta(date.today(), self.dob)

    @property
    def working_days(self):
        return {'monday': self.works_monday,
                'tuesday': self.works_tuesday,
                'wednesday': self.works_wednesday,
                'thursday': self.works_thursday,
                'friday': self.works_friday}


class Address(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    rel = models.IntegerField(choices=ADDRESS_RELS)
    postal = models.BooleanField(default=False)
    label = models.CharField(max_length=255)
    primary = models.BooleanField()
    postcode = models.IntegerField()
    state = models.CharField(max_length=255, choices=STATES)
    suburb = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pobox = models.BooleanField(default=False)
    number = models.CharField(max_length=50)  # This is a string to accomodate numbers like 15A
    street = models.CharField(max_length=255)
    staff_member = models.ForeignKey('StaffMember', related_name='addresses')


class PhoneNumber(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    rel = models.IntegerField(choices=PHONE_RELS)
    label = models.CharField(max_length=255)
    primary = models.BooleanField(default=False)
    value = models.IntegerField()

    class Meta:
        abstract = True
        ordering = ['primary']


class StaffPhoneNumber(PhoneNumber):
    staff_member = models.ForeignKey('StaffMember', related_name='phone_numbers')


class NOKPhoneNumber(PhoneNumber):
    next_of_kin = models.ForeignKey('NextOfKin', related_name='phone_numbers')


class NextOfKin(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    title = models.CharField(max_length=50, choices=COMMON_TITLES)
    given_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    # phone_numbers back reference
    staff_member = models.ForeignKey('StaffMember', related_name='next_of_kin')


class Qualification(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    label = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    date_awarded = models.DateField()
    staff_member = models.ForeignKey('StaffMember', related_name='qualifications')


class EmailAddress(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    address = models.EmailField(max_length=255)
    label = models.CharField(max_length=255)
    rel = models.IntegerField(choices=ADDRESS_RELS)
    primary = models.BooleanField(default=False)
    staff_member = models.ForeignKey('StaffMember', related_name='email_addresses')

