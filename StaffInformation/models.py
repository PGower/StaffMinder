from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta
import reversion


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

STATES = [('QLD', 'Queensland'),
          ('NSW', 'New South Wales'),
          ('VIC', 'Victoria'),
          ('TAS', 'Tasmania'),
          ('WA', 'Western Australia'),
          ('SA', 'South Australia'),
          ('ACT', 'Australian Capitol Territory'),
          ('NT', 'Northern Territory'),
          ('OTHER', 'Outside Australia')]


class StaffMemberQuerySet(models.query.QuerySet):
    def delete(self):
        # TODO: this should generate sql that sets the active attribute to false rather than deleting records
        pass


class StaffMemberModelManager(models.Manager):
    def get_queryset(self):
        return StaffMemberQuerySet(self.model, using=self._db).filter(active=True)


class StaffMember(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    title = models.CharField(max_length=50, choices=COMMON_TITLES)
    prefered_given_name = models.CharField(max_length=255, blank=True, null=True,
                                           help_text='Prefered first name if different to legal first name',
                                           verbose_name='Prefered Given Name')
    legal_given_name = models.CharField(max_length=255,
                                        help_text='Legal first name as shown on birth certificate',
                                        verbose_name='Legal Given Name')
    middle_name = models.CharField(max_length=255, blank=True, null=True,
                                   verbose_name='Middle Name')
    prefered_surname = models.CharField(max_length=255, blank=True, null=True,
                                        help_text='Prefered surname if different to legal surname',
                                        verbose_name='Prefered Surname')
    legal_surname = models.CharField(max_length=255,
                                     help_text='Legal surname as shown on birth certificate',
                                     verbose_name='Legal Surname')
    # addresses back reference
    # phone_numbers back reference
    # email_addresses back reference
    dob = models.DateField(verbose_name='Date of Birth')
    religion = models.CharField(max_length=255, blank=True, null=True,
                                help_text='Leave blank if religion is unknown')
    teacher_registration_number = models.IntegerField(unique=True, blank=True, null=True,
                                                      help_text='Leave blank if unknown or not applicable',
                                                      verbose_name='Teacher Registration Number')
    teacher_registration_expiry = models.DateField(blank=True, null=True,
                                                   help_text='Leave blank if unknown or not applicable',
                                                   verbose_name='Teacher Registration Expiry')
    # subjects taught
    timetable_code = models.CharField(max_length=50, unique=True, blank=True, null=True,
                                      help_text='Teacher code as used in The Timetabler if applicable',
                                      verbose_name='Timetable Code')
    employee_number = models.CharField(max_length=255, unique=True,
                                       help_text='Staff employee number',
                                       verbose_name='Staff Employee Number')
    bluecard_number = models.CharField(max_length=255, unique=True,
                                       help_text='Blue Card Registration Number',
                                       verbose_name='Blue Card Number')
    bluecard_expiry = models.DateField(help_text='Blue Card Expiry',
                                       verbose_name='Blue Card Expiry')
    # next_of_kin back reference
    vehicle_registration = models.CharField(max_length=50, blank=True, null=True,
                                            help_text='Vehicle registration number if applicable',
                                            verbose_name='Vehicle Registration')
    media_consent_form = models.BooleanField(default=False,
                                             help_text='Check if your media consent form has been flled out and returned to the school',
                                             verbose_name='Media Consent Form')
    weekly_hours_worked = models.IntegerField(default=38,
                                              help_text='Number of hours worked per week',
                                              verbose_name='Weekly Hours Worked')
    works_monday = models.BooleanField(default=True, verbose_name='Works Monday')
    works_tuesday = models.BooleanField(default=True, verbose_name='Works Tuesday')
    works_wednesday = models.BooleanField(default=True, verbose_name='Works Wednesday')
    works_thursday = models.BooleanField(default=True, verbose_name='Works Thrusday')
    works_friday = models.BooleanField(default=True, verbose_name='Works Friday')
    # qualifications back reference
    active = models.BooleanField(default=True)

    # Custom object manager, only shows active staff members
    objects = StaffMemberModelManager()

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

    def delete(self, *args, **kwargs):
        '''Prevent deletion of StaffMember objects, just set active = false'''
        self.active = False
        self.save()

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'
        ordering = ('legal_surname', 'legal_given_name')


reversion.register(StaffMember)


class Address(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    rel = models.IntegerField(choices=ADDRESS_RELS, verbose_name='Kind')
    postal = models.BooleanField(default=False,
                                 help_text='Is this a postal address?',
                                 verbose_name='Postal Address')
    label = models.CharField(max_length=255,
                             help_text='A short description for this address')
    primary = models.BooleanField(help_text='Is this address your primary address?')
    postcode = models.IntegerField(help_text='The address postcode')
    state = models.CharField(max_length=255, choices=STATES)
    suburb = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pobox = models.BooleanField(default=False,
                                help_text='Is this address a PO Box?',
                                verbose_name='PO Box')
    number = models.CharField(max_length=50)  # This is a string to accomodate numbers like 15A
    street = models.CharField(max_length=255)
    staff_member = models.ForeignKey('StaffMember', related_name='addresses')

    def save(self, *args, **kwargs):
        '''If this email address is chosen as the primary address then update any
        other EmailAddress for this staff member that is marked as primary'''
        if self.primary is True:
            Address.objects.filter(primary=True, staff_member=self.staff_member).update(primary=False)
        super(Address, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.primary is True:
            try:
                e = Address.objects.filter(primary=False, staff_member=self.staff_member).all()[0]
                e.primary = True
                e.save()
            except IndexError:
                pass
        super(Address, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Staff Address'
        verbose_name_plural = 'Staff Addresses'
        ordering = ('primary', 'updated')


reversion.register(Address)


class PhoneNumber(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    rel = models.IntegerField(choices=PHONE_RELS, verbose_name='Kind')
    label = models.CharField(max_length=255, blank=True, null=True)
    primary = models.BooleanField(default=False)
    value = models.IntegerField(verbose_name='Number')

    class Meta:
        abstract = True
        ordering = ['primary', 'updated']


class StaffPhoneNumber(PhoneNumber):
    staff_member = models.ForeignKey('StaffMember', related_name='phone_numbers')

    def save(self, *args, **kwargs):
        '''If this email address is chosen as the primary address then update any
        other EmailAddress for this staff member that is marked as primary'''
        if self.primary is True:
            StaffPhoneNumber.objects.filter(primary=True, staff_member=self.staff_member).update(primary=False)
        super(StaffPhoneNumber, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.primary is True:
            try:
                e = StaffPhoneNumber.objects.filter(primary=False, staff_member=self.staff_member).all()[0]
                e.primary = True
                e.save()
            except IndexError:
                pass
        super(StaffPhoneNumber, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Staff Phone Number'
        verbose_name_plural = 'Staff Phone Numbers'


reversion.register(StaffPhoneNumber)


class NOKPhoneNumber(PhoneNumber):
    next_of_kin = models.ForeignKey('NextOfKin', related_name='phone_numbers')

    def save(self, *args, **kwargs):
        '''If this email address is chosen as the primary address then update any
        other EmailAddress for this staff member that is marked as primary'''
        if self.primary is True:
            NOKPhoneNumber.objects.filter(primary=True, next_of_kin=self.next_of_kin).update(primary=False)
        super(NOKPhoneNumber, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.primary is True:
            try:
                e = NOKPhoneNumber.objects.filter(primary=False, next_of_kin=self.next_of_kin).all()[0]
                e.primary = True
                e.save()
            except IndexError:
                pass
        super(NOKPhoneNumber, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Next of Kin Phone Number'
        verbose_name_plural = 'Next of Kin Phone Numbers'


reversion.register(NOKPhoneNumber)


class NextOfKin(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    title = models.CharField(max_length=50, choices=COMMON_TITLES)
    given_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255,
                                    help_text='How this person is related to you')
    priority = models.IntegerField(help_text='The order in which your Next of Kin contacts should be contacted')
    # phone_numbers back reference
    staff_member = models.ForeignKey('StaffMember', related_name='next_of_kin')

    class Meta:
        unique_together = [('staff_member', 'priority')]
        verbose_name = 'Next of Kin'
        verbose_name_plural = 'Next of Kin'
        ordering = ('priority',)


reversion.register(NextOfKin)


class Qualification(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    label = models.CharField(max_length=255, help_text='A short description for this qualification.')
    institution = models.CharField(max_length=255, help_text='The institution which you recieved this qualification through.')
    date_awarded = models.DateField(help_text='The date this qualification was awarded to you')
    staff_member = models.ForeignKey('StaffMember', related_name='qualifications')

    class Meta:
        verbose_name = 'Qualification'
        verbose_name_plural = 'Qualifications'


reversion.register(Qualification)


class EmailAddress(models.Model):
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    address = models.EmailField(max_length=255, verbose_name='Email Address')
    label = models.CharField(max_length=255)
    rel = models.IntegerField(choices=ADDRESS_RELS, verbose_name='Kind')
    primary = models.BooleanField(default=False)
    staff_member = models.ForeignKey('StaffMember', related_name='email_addresses')

    def save(self, *args, **kwargs):
        '''If this email address is chosen as the primary address then update any
        other EmailAddress for this staff member that is marked as primary'''
        if self.primary is True:
            EmailAddress.objects.filter(primary=True, staff_member=self.staff_member).update(primary=False)
        super(EmailAddress, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.primary is True:
            try:
                e = EmailAddress.objects.filter(primary=False, staff_member=self.staff_member).all()[0]
                e.primary = True
                e.save()
            except IndexError:
                pass
        super(EmailAddress, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Staff Email Address'
        verbose_name_plural = 'Staff Email Addresses'
        ordering = ('primary', 'updated')


reversion.register(EmailAddress)
