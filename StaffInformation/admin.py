from django.contrib import admin
import reversion

from models import (StaffMember,
                    Address,
                    StaffPhoneNumber,
                    NOKPhoneNumber,
                    NextOfKin,
                    Qualification,
                    EmailAddress)


class InlineAddressAdmin(admin.StackedInline):
    model = Address
    extra = 1
    fields = ('rel', 'label', 'number', 'street', 'suburb',
              'city', 'state', 'postcode', 'primary',
              'pobox')


class InlineStaffPhoneNumberAdmin(admin.TabularInline):
    model = StaffPhoneNumber
    extra = 3
    fields = ('rel', 'label', 'value', 'primary')


class InlineQualificationAdmin(admin.TabularInline):
    model = Qualification
    extra = 3
    fields = ('label', 'institution', 'date_awarded')


class InlineEmailAddressAdmin(admin.TabularInline):
    model = EmailAddress
    extra = 3
    fields = ('rel', 'label', 'address', 'primary')


class InlineNOKAdmin(admin.TabularInline):
    model = NextOfKin
    extra = 1
    fields = ('title', 'given_name', 'surname', 'relationship', 'priority')


class StaffMemberAdmin(reversion.VersionAdmin):
    model = StaffMember
    history_latest_first = True
    fieldsets = [('Name', {'fields':('title',
                                    'prefered_given_name',
                                    'legal_given_name',
                                    'middle_name',
                                    'prefered_surname',
                                    'legal_surname')}),
                ('Birth Date', {'fields':('dob',)}),
                ('Religion', {'fields':('religion',)}),
                ('Teacher Registration', {'fields':('teacher_registration_number',
                                                   'teacher_registration_expiry')}),
                ('Timetable', {'fields':('timetable_code',)}),
                ('HR Details', {'fields':('employee_number','media_consent_form')}),
                ('Blue Card', {'fields':('bluecard_number','bluecard_expiry')}),
                ('Vehicle Details', {'fields':('vehicle_registration',)}),
                ('Work Schedule', {'fields':('weekly_hours_worked','works_monday','works_tuesday','works_wednesday','works_thursday','works_friday')})
    ]
    inlines = (InlineAddressAdmin,
               InlineStaffPhoneNumberAdmin,
               InlineQualificationAdmin,
               InlineEmailAddressAdmin,
               InlineNOKAdmin)


class AddressAdmin(admin.ModelAdmin):
    model = Address


class StaffPhoneNumberAdmin(admin.ModelAdmin):
    model = StaffPhoneNumber


class NOKPhoneNumberAdmin(admin.ModelAdmin):
    model = NOKPhoneNumber


class NextOfKinAdmin(admin.ModelAdmin):
    model = NextOfKin


class QualificationAdmin(admin.ModelAdmin):
    model = Qualification


class EmailAddressAdmin(admin.ModelAdmin):
    model = EmailAddress


admin.site.register(StaffMember, StaffMemberAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(StaffPhoneNumber, StaffPhoneNumberAdmin)
admin.site.register(NOKPhoneNumber, NOKPhoneNumberAdmin)
admin.site.register(NextOfKin, NextOfKinAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(EmailAddress, EmailAddressAdmin)